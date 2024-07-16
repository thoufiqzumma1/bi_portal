# Import library
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import re
import numpy as np

# Load dataset
st.set_page_config(layout='wide')
df = pd.read_csv('/content/drive/MyDrive/Streamlit/1st/transaction/file.csv')

# Remove space at the top
st.markdown(
    """
    <style>
    .main > div {
        padding-top: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="blue-bg"><h1 class="centered-title">Hello, Streamlit!</h1></div>', unsafe_allow_html=True)

# Filter DataFrame by date (assuming 'transaction_date' is your date column)
min_date = pd.to_datetime(df['transaction_date']).min().date()
max_date = pd.to_datetime(df['transaction_date']).max().date()

d1, d2 = st.columns([1, 1])
# Date range input
with d1:
    start_date = st.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date)
with d2:
    end_date = st.date_input("End date", min_value=start_date, max_value=max_date, value=max_date)

# Filter DataFrame by date range
filtered_df = df[(pd.to_datetime(df['transaction_date']).dt.date >= start_date) &
                 (pd.to_datetime(df['transaction_date']).dt.date <= end_date)]



# Ensure 'Agency Code' is a string
filtered_df['agent_id'] = filtered_df['agent_id'].astype(str)

# Add a text input for the agent code
agent_id = st.text_input('agent_id')

# Filter DataFrame by agent code if provided
if agent_id:
    filtered_df = filtered_df[filtered_df['agent_id'].str.contains(agent_id, case=False, na=False)]


# Function to create a KPI card with dynamic values
def card_view(title, value1, value2, color1, color2):
    st.markdown(
        f"""
        <div style="padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 24px;">{title}</h2>
            <div style="display: flex; justify-content: space-around;">
                <div style="background-color: {color1}; padding: 10px; border-radius: 5px; width: 45%; color: white;">
                    <p style="margin: 5px 0 0; font-size: 18px;">{value1}</p>
                </div>
                <div style="background-color: {color2}; padding: 10px; border-radius: 5px; width: 45%; color: white;">
                    <p style="margin: 5px 0 0; font-size: 18px;">{value2}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Aggregate KPI metrics
aggregated_kpi_data = {
    "initialdeposit": filtered_df["initialdeposit"].sum(),
    "initialdeposit_amount": filtered_df["initialdeposit_amount"].sum(),
    "qrcharge": filtered_df["qrcharge"].sum(),
    "qrcharge_amount": filtered_df["qrcharge_amount"].sum(),
    "selfdeposit": filtered_df["selfdeposit"].sum(),
     "selfdeposit_amount": filtered_df["selfdeposit_amount"].sum(),
    "bearerdeposit": filtered_df["bearerdeposit"].sum(),
    "bearerdeposit_amount": filtered_df["bearerdeposit_amount"].sum(),
    "transfer": filtered_df["transfer"].sum(),
    "transfer_amount": filtered_df["transfer_amount"].sum(),
    "withdrawal": filtered_df["withdrawal"].sum(),
    "withdrawal_amount": filtered_df["withdrawal_amount"].sum(),
    "ifrwithdrawal": filtered_df["ifrwithdrawal"].sum(),
    "ifrwithdrawal_amount": filtered_df["ifrwithdrawal_amount"].sum(),
    "jalalabadgasbill": filtered_df["jalalabadgasbill"].sum(),
    "jalalabadgasbill_amount": filtered_df["jalalabadgasbill_amount"].sum(),
    "bakhrabadbilldeposit": filtered_df["bakhrabadbilldeposit"].sum(),
    "bakhrabadbilldeposit_amount": filtered_df["bakhrabadbilldeposit_amount"].sum(),
    "reb_bill": filtered_df["reb_bill"].sum(),
    "reb_bill_amount": filtered_df["reb_bill_amount"].sum(),
}

# Define KPI metrics, colors, and fetch data from df
kpi_data = [
    {"title": "Initial Deposit", "value1": aggregated_kpi_data["initialdeposit"], "value2": aggregated_kpi_data["initialdeposit_amount"],
     "color1": "#4CAF50", "color2": "#FF9800"},
    {"title": "QR Charge", "value1": aggregated_kpi_data["qrcharge"], "value2": aggregated_kpi_data["qrcharge_amount"],
     "color1": "#2196F3", "color2": "#E91E63"},
    {"title": "Self Deposit", "value1": aggregated_kpi_data["selfdeposit"], "value2": aggregated_kpi_data["selfdeposit_amount"], "color1": "#FFC107",
     "color2": "#607D8B"},
    {"title": "Bearer Deposit", "value1": aggregated_kpi_data["bearerdeposit"], "value2": aggregated_kpi_data["bearerdeposit_amount"],
     "color1": "#9C27B0", "color2": "#673AB7"},
    {"title": "Transfer", "value1": aggregated_kpi_data["transfer"], "value2": aggregated_kpi_data["transfer_amount"],
     "color1": "#FF5722", "color2": "#FF5722"},
    {"title": "Withdrawal", "value1": aggregated_kpi_data["withdrawal"], "value2": aggregated_kpi_data["withdrawal_amount"],
     "color1": "#FF9800", "color2": "#4CAF50"},
    {"title": "IFR Withdrawal", "value1": aggregated_kpi_data["ifrwithdrawal"], "value2": aggregated_kpi_data["ifrwithdrawal_amount"],
     "color1": "#E91E63", "color2": "#2196F3"},
    {"title": "Jalalabad Gas Bill", "value1": aggregated_kpi_data["jalalabadgasbill"],
     "value2": aggregated_kpi_data["jalalabadgasbill_amount"], "color1": "#607D8B", "color2": "#FFC107"},
    {"title": "Bakhrabad Bill Deposit", "value1": aggregated_kpi_data["bakhrabadbilldeposit"],
     "value2": aggregated_kpi_data["bakhrabadbilldeposit_amount"], "color1": "#673AB7", "color2": "#9C27B0"},
    {"title": "REB Bill", "value1": aggregated_kpi_data["reb_bill"], "value2": aggregated_kpi_data["reb_bill_amount"],
     "color1": "#009688", "color2": "#FF5722"}
]

# Creating columns for KPI cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    card_view(
        title=kpi_data[0]["title"],
        value1=kpi_data[0]["value1"],
        value2=kpi_data[0]["value2"],
        color1=kpi_data[0]["color1"],
        color2=kpi_data[0]["color2"]
    )

with col2:
    card_view(
        title=kpi_data[1]["title"],
        value1=kpi_data[1]["value1"],
        value2=kpi_data[1]["value2"],
        color1=kpi_data[1]["color1"],
        color2=kpi_data[1]["color2"]
    )

with col3:
    card_view(
        title=kpi_data[2]["title"],
        value1=kpi_data[2]["value1"],
        value2=kpi_data[2]["value2"],
        color1=kpi_data[2]["color1"],
        color2=kpi_data[2]["color2"]
    )

with col4:
    card_view(
        title=kpi_data[3]["title"],
        value1=kpi_data[3]["value1"],
        value2=kpi_data[3]["value2"],
        color1=kpi_data[3]["color1"],
        color2=kpi_data[3]["color2"]
    )

with col5:
    card_view(
        title=kpi_data[4]["title"],
        value1=kpi_data[4]["value1"],
        value2=kpi_data[4]["value2"],
        color1=kpi_data[4]["color1"],
        color2=kpi_data[4]["color2"]
    )

col6, col7, col8, col9, col10 = st.columns(5)

with col6:
    card_view(
        title=kpi_data[5]["title"],
        value1=kpi_data[5]["value1"],
        value2=kpi_data[5]["value2"],
        color1=kpi_data[5]["color1"],
        color2=kpi_data[5]["color2"]
    )

with col7:
    card_view(
        title=kpi_data[6]["title"],
        value1=kpi_data[6]["value1"],
        value2=kpi_data[6]["value2"],
        color1=kpi_data[6]["color1"],
        color2=kpi_data[6]["color2"]
    )

with col8:
    card_view(
        title=kpi_data[7]["title"],
        value1=kpi_data[7]["value1"],
        value2=kpi_data[7]["value2"],
        color1=kpi_data[7]["color1"],
        color2=kpi_data[7]["color2"]
    )

with col9:
    card_view(
        title=kpi_data[8]["title"],
        value1=kpi_data[8]["value1"],
        value2=kpi_data[8]["value2"],
        color1=kpi_data[8]["color1"],
        color2=kpi_data[8]["color2"]
    )

with col10:
    card_view(
        title=kpi_data[9]["title"],
        value1=kpi_data[9]["value1"],
        value2=kpi_data[9]["value2"],
        color1=kpi_data[9]["color1"],
        color2=kpi_data[9]["color2"]
    )

# Multi-select for columns to display
selected_columns = st.multiselect(
    "Select columns to display",
    ['agent_id', 'Cluster', 'BDEx Name', 'Csp Name',
     'Official mail', 'Trade Name', 'Branch Name', 'Branch Mail', 'Location',
     'Gender', 'Agency Code', 'initialdeposit', 'initialdeposit_amount',
     'qrcharge', 'qrcharge_amount', 'selfdeposit', 'selfdeposit_amount',
     'bearerdeposit', 'bearerdeposit_amount', 'transfer', 'transfer_amount',
     'withdrawal', 'withdrawal_amount', 'ifrwithdrawal', 'ifrwithdrawal_amount',
     'jalalabadgasbill', 'jalalabadgasbill_amount', 'bakhrabadbilldeposit',
     'bakhrabadbilldeposit_amount', 'reb_bill', 'reb_bill_amount', 'rtgs',
     'rtgs_amount', 'nescobilldeposit', 'nescobilldeposit_amount', 'pranrflcharge',
     'pranrflcharge_amount', 'islamiarabiccharge', 'islamiarabiccharge_amount'],
    default=['agent_id', 'Cluster', 'BDEx Name', 'Csp Name',
             'Official mail', 'Trade Name', 'Branch Name', 'Branch Mail', 'Location',
             'Gender', 'Agency Code']
)

# # Filter DataFrame columns based on selected columns
# filtered_df = filtered_df[selected_columns]

# # Assuming filtered_df is your DataFrame
# filtered_df_with_index = filtered_df.reset_index(drop=True)
# st.dataframe(filtered_df_with_index)


import numpy as np
filtered_df = filtered_df[selected_columns]
filtered_df_with_index = filtered_df.reset_index(drop=True)
grand_total = filtered_df_with_index.select_dtypes(include=[np.number]).sum()
grand_total_row = {col: '' for col in filtered_df_with_index.columns}
grand_total_row.update(grand_total)
grand_total_row['Cluster'] = 'Grand Total'
grand_total_df = pd.DataFrame([grand_total_row])
filtered_df_with_index = pd.concat([filtered_df_with_index, grand_total_df], ignore_index=True)
st.dataframe(filtered_df_with_index)







