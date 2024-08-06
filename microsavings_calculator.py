import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# assumptions

#average_days_in_month = 30.437
days_in_month = 30

def calculate_balance_and_capital(initial_deposit, interest_rates, savings_period,
    daily_top_up, days_in_month):
    balance = [initial_deposit]
    total_top_ups = 0
    interest_rate_day = []

    for day in range(1, int(savings_period*days_in_month) + 1):
        daily_balance = balance[-1]

        # Find the corresponding interest rate based on the balance
        for i in range(len(interest_rates["Saldo mínimo"])):
            if interest_rates["Saldo mínimo"]\
            [i] <= daily_balance < interest_rates["Saldo máximo"][i]:
                daily_interest_rate = (1 + interest_rates[
                    "TANB (%)"][i] / 100) ** (1 / 360) - 1
                day_rate = interest_rates["TANB (%)"][i]
                break

        interest_rate_day.append(day_rate) # TANB corresponding to balance on given day

        daily_balance *= (1 + daily_interest_rate)  # compounding interest daily

        # Add daily top-ups
        daily_balance += daily_top_up
        total_top_ups += daily_top_up

        balance.append(daily_balance)

    last_day_rate = interest_rate_day[-1] # correct for mismatch between 
    interest_rate_day.append(last_day_rate) # day zero and last day in range

    total_capital = initial_deposit + total_top_ups
    total_gains = balance[-1] - total_capital

    return balance, total_capital, total_gains, interest_rate_day

def calculate_daily_top_up(initial_deposit, savings_period,
    savings_target, days_in_month):
    # Calculate the remaining amount needed to reach the savings target
    remaining_amount = savings_target - initial_deposit

    # Calculate the equivalent daily top-up needed to reach the target within the specified period
    daily_top_up = int(remaining_amount / (savings_period * days_in_month))

    return daily_top_up

def main():

    # Title
    st.title(f'Simulador de micropoupanças :money_with_wings: :bulb:')

    # Sidebar for user inputs
    st.sidebar.header("Fatores")
    savings_target = st.sidebar.number_input("Objetivo de poupança:", min_value=0.01, value=300000.0)
    initial_deposit = st.sidebar.number_input("Depósito inicial:",
        min_value=0.01, value=10000.0)
    savings_period = st.sidebar.slider("Prazo (meses):",
        min_value=1, max_value=36, value=6, step=1)
    time_unit = st.sidebar.radio("Mostrar resultados em", ["Meses", "Dias"])

    # Calculate daily top-up based on savings target
    daily_top_up = calculate_daily_top_up(initial_deposit,
        savings_period, savings_target, days_in_month)

    # Display calculated daily top-up and allow user input
    daily_top_up = st.sidebar.number_input("""Média de acréscimos diários para poupar até o
        objetivo (descontado o depóstio inicial). Pode ser ajustado:""",
        min_value=0, value=daily_top_up)

    st.sidebar.markdown("Escalões de Taxa Anual Nominal Bruta:")
    annual_interest_rate = st.sidebar.data_editor(
        {"Saldo mínimo": [0.0, 25000.0, 75000.0, 150000.0, 300000.0], 
        "Saldo máximo": [25000.0, 75000.0, 150000.0, 300000.0, 1000000.0],
        "TANB (%)": [10.0, 12.5, 15.0, 17.5, 20.0]})

    # Calculate account balance, total capital, and total gains
    balance_data, total_capital, total_gains, interest_rate_day = calculate_balance_and_capital(
        initial_deposit, annual_interest_rate, savings_period, daily_top_up, days_in_month)

    # Display the graph corresponding with selected time unit
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if time_unit == "Meses":
        # Display the result as a line graph over months
        months = np.arange(0, savings_period + 1, 1)
        days_per_month = days_in_month
        days = months * days_per_month

        # Select every int(days_in_month)-th element backwards in balance_data and TANB
        selected_balance_data = balance_data[::-int(days_in_month)]
        selected_rates = interest_rate_day[::-int(days_in_month)]

        df = pd.DataFrame({"Dias": days[:len(selected_balance_data)],
            "Meses": months[:len(selected_balance_data)],
            "Saldo": selected_balance_data[::-1],
            "TANB": selected_rates[::-1]})

        # Add traces
        fig.add_trace(
            go.Scatter(x=df["Meses"], y=df["Saldo"], name="Saldo (Kz)"),
            secondary_y=False,
            )

        fig.add_trace(
            go.Scatter(x=df["Meses"], y=df["TANB"], name="TANB (%)"),
            secondary_y=True,
            )

        # Set x-axis title
        fig.update_xaxes(title_text="Meses")

    else:
        # Display the result as a line graph over days
        days = range(0, int(savings_period*days_in_month) + 1)

        df = pd.DataFrame({"Dias": days,
            "Saldo": balance_data,
            "TANB": interest_rate_day})

        # Add traces
        fig.add_trace(
            go.Scatter(x=df["Dias"], y=df["Saldo"], name="Saldo (Kz)"),
            secondary_y=False,
            )

        fig.add_trace(
            go.Scatter(x=df["Dias"], y=df["TANB"], name="TANB (%)"),
            secondary_y=True,
            )

        # Set x-axis title
        fig.update_xaxes(title_text="Dias")

    # Add legend title
    fig.update_layout(legend_title_text='Evolução de:')

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Saldo</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>TANB (%)</b>", secondary_y=True)
    
    # Display the graph
    st.plotly_chart(fig, use_container_width=True)  # Set use_container_width to True to centre

    # Display total capital and total gains
    st.subheader("Resumo:")
    st.markdown(f"**-> Capital acumulado:** {(total_capital+total_gains):,.2f}")
    st.write(f"-> Dinheiro poupado: {total_capital:,.2f}")
    st.write(f"-> Juros vencidos: {total_gains:,.2f}")

if __name__ == "__main__":
    main()
