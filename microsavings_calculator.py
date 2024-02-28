import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# assumptions

#average_days_in_month = 30.437
days_in_month = 30

def calculate_balance_and_capital(initial_deposit, annual_interest_rate, savings_period,
    daily_top_up, days_in_month):
    balance = [initial_deposit]
    daily_interest_rate = (1 + annual_interest_rate / 100) ** (1 / 360) - 1
    total_top_ups = 0

    for day in range(1, int(savings_period*days_in_month) + 1):
        daily_balance = balance[-1]
        daily_balance *= (1 + daily_interest_rate)  # compounding interest daily

        # Add daily top-ups
        daily_balance += daily_top_up
        total_top_ups += daily_top_up

        balance.append(daily_balance)

    total_capital = initial_deposit + total_top_ups
    total_gains = balance[-1] - total_capital

    return balance, total_capital, total_gains

def calculate_daily_top_up(initial_deposit, annual_interest_rate, savings_period,
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
    annual_interest_rate = st.sidebar.number_input("Taxa Anual Nominal Bruta (TANB, %):",
        min_value=0.01, value=10.0)

    # Calculate daily top-up based on savings target
    daily_top_up = calculate_daily_top_up(initial_deposit, annual_interest_rate,
        savings_period, savings_target, days_in_month)

    # Display calculated daily top-up and allow user input
    daily_top_up = st.sidebar.number_input("""Média de acréscimos diários para poupar até o
        objetivo (descontado o depóstio inicial). Pode ser ajustado:""",
        min_value=0, value=daily_top_up)

    # Calculate account balance, total capital, and total gains
    balance_data, total_capital, total_gains = calculate_balance_and_capital(initial_deposit, 
        annual_interest_rate, savings_period, daily_top_up, days_in_month)

    # Display the result as a line graph
    months = np.arange(0, savings_period + 1, 1)
    days_per_month = days_in_month
    days = months * days_per_month

    # Select every int(days_in_month)-th element backwards in balance_data
    selected_balance_data = balance_data[::-int(days_in_month)]

    df = pd.DataFrame({"Dias": days[:len(selected_balance_data)],
        "Meses": months[:len(selected_balance_data)],
        "Saldo": selected_balance_data[::-1]})

    fig = px.line(df[df["Meses"] <= int(savings_period*days_in_month)],
        x="Meses", y="Saldo",
        #title="Vencimento"
        )
    
    # Display the graph
    st.plotly_chart(fig, use_container_width=True)  # Set use_container_width to True to centre

    # Display total capital and total gains
    st.subheader("Resumo:")
    st.markdown(f"**-> Capital acumulado:** {(total_capital+total_gains):,.2f}")
    st.write(f"-> Dinheiro poupado: {total_capital:,.2f}")
    st.write(f"-> Juros vencidos: {total_gains:,.2f}")

if __name__ == "__main__":
    main()
