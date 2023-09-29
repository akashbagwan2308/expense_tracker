# Import necessary libraries
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import io

# Function to load the existing data from the Excel file
def load_data():
    try:
        df = pd.read_excel("expenditure.xlsx", parse_dates=["Date"])  # Parse "Date" column as datetime
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "Description", "Amount", "Category", "Balance"])
    return df

# Function to save the data to the Excel file
def save_data(df):
    df.to_excel("expenditure.xlsx", index=False)

# Create a Streamlit app
def main():
    st.title("Expense Tracking Web App")

    # Load existing data or create a new DataFrame
    df = load_data()

    # Sidebar for adding new expenditure
    st.sidebar.header("Add New Expense/Deposit")
    date = st.sidebar.date_input("Date", datetime.date.today())
    description = st.sidebar.text_input("Description")
    amount = st.sidebar.number_input("Amount ($)", value=0.0)

    # Add a category dropdown in the sidebar
    category = st.sidebar.selectbox("Category", [
        "Nashta", "Lunch", "Eve.Break", "Dinner", "Off Dinner",
        "Personal/Rent", "E - Bill", "Recharges", "Grocery",
        "Travel Exchange", "Stationary", "Deposit"  # Added "Deposit" category
    ])

    if st.sidebar.button("Add"):
        if amount != 0:
            # Convert the date to a string format
            date_str = date.strftime('%Y-%m-%d')

            # Calculate balance
            if category == "Deposit":
                balance = df["Balance"].iloc[-1] + amount
            else:
                balance = df["Balance"].iloc[-1] - amount

            new_data = {
                "Date": [date_str],
                "Description": [description],
                "Amount": [amount],
                "Category": [category],
                "Balance": [balance]  # Added "Balance" column
            }
            df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
            save_data(df)
            st.success("Expense added successfully!")

    # Button to show the complete table
    if st.button("Show Complete Table"):
        st.header("Complete Table of Expenditure")
        st.table(df)

    # Display the last 5 rows of the expenditure table
    Month = ['January','February','March','April','May','June','July','August','September','October','November','December']
    month = Month[int(date.strftime('%m'))-1]
    st.header(f"Last 5 Rows of Expense Table {month}")
    st.table(df.tail(5))  # Display the last 5 rows

    # Add a download button to download the Excel file
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    excel_buffer.seek(0)
    st.download_button("Download Excel File", excel_buffer, file_name="expenditure.xlsx", key="download-button")

    # Calculate and display the total expenditure
    total_expenditure = df[df["Category"] != "Deposit"]["Amount"].sum()
    st.subheader(f"Total Expense: ₹ {total_expenditure:.2f}")

    # Calculate and display the current balance
    current_balance = df["Balance"].iloc[-1]
    st.subheader(f"Current Balance: ₹ {current_balance:.2f}")

    # Create a donut chart to visualize expenses by category
    category_expenses = df.groupby("Category")["Amount"].sum().reset_index()
    category_expenses.rename(columns={"Amount": "Total Amount"}, inplace=True)

    st.header("Expenses by Category : ")
    fig = px.pie(category_expenses, values="Total Amount", names="Category", hole=0.39)
    st.plotly_chart(fig)



if __name__ == "__main__":
    main()
