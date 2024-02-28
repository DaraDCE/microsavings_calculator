## README

This is a Streamlit app designed to help you simulate your micro-savings journey. 

**Features:**

* **Goal Setting:** Define your desired savings target.
* **Initial Deposit:** Enter your initial deposit amount.
* **Saving Period:** Specify the desired saving period in months.
* **Interest Rate:** Set the annual interest rate offered by your savings account.
* **Daily Top-Up Calculation:** The app calculates the recommended daily top-up amount needed to reach your savings target within the specified timeframe, based on the initial deposit and interest rate.
* **Top-Up Adjustment:** You can adjust the calculated daily top-up amount to suit your preferences.
* **Visualization:** The app generates a line graph to visualize your account balance growth over time.
* **Summary:** The app displays the total capital accumulated, including your deposits and earned interest, along with the breakdown of your saved amount and earned interest.

**Requirements:**

* Python 3.x
* Streamlit library ([https://streamlit.io/](https://streamlit.io/))
* Pandas library ([https://pandas.pydata.org/](https://pandas.pydata.org/))
* NumPy library ([https://numpy.org/](https://numpy.org/))
* Plotly library ([https://plotly.com/python/](https://plotly.com/python/))

**How to Use:**

1. Clone or download the repository containing the app files.
2. Install the required libraries using `pip install streamlit pandas numpy plotly`.
3. Open a terminal or command prompt and navigate to the directory containing the app files.
4. Run the app using `streamlit run app.py`.

**Notes:**

* This is a simple simulation tool and does not consider real-world factors like inflation or fees.
* The provided assumptions, such as the average number of days in a month, can be adjusted based on your specific needs.
