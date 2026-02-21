import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="SHREY CAB SERVICES",
                   page_icon="🚖",
                   layout="wide")

st.title("🚖 SHREY CAB SERVICES – Business Dashboard")

# ----------- Create Blank Template -----------
def create_template():
    return pd.DataFrame({
        "Booking_ID": [],
        "Customer_Name": [],
        "City": [],
        "Cab_Type": [],
        "Trip_Date": [],
        "Fare_Amount": []
    })

def convert_to_excel(df):
    output = BytesIO()
    df.to_excel(output, index=False)
    return output.getvalue()

template = create_template()

st.download_button(
    "📥 Download Blank Excel Template",
    data=convert_to_excel(template),
    file_name="SHREY_CAB_TEMPLATE.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.divider()

# ----------- Upload File -----------
uploaded_file = st.file_uploader("📤 Upload Filled Excel File", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.dataframe(df)

    total_bookings = len(df)
    total_revenue = df["Fare_Amount"].sum()
    avg_fare = df["Fare_Amount"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Bookings", total_bookings)
    col2.metric("Total Revenue", f"₹ {total_revenue}")
    col3.metric("Average Fare", f"₹ {round(avg_fare,2)}")

    # Pie Chart - Revenue by City
    city_revenue = df.groupby("City")["Fare_Amount"].sum().reset_index()

    fig1 = px.pie(city_revenue,
                  names="City",
                  values="Fare_Amount",
                  title="Revenue by City")
    st.plotly_chart(fig1)

    # Pie Chart - Cab Type
    cab_count = df["Cab_Type"].value_counts().reset_index()
    cab_count.columns = ["Cab_Type", "Count"]

    fig2 = px.pie(cab_count,
                  names="Cab_Type",
                  values="Count",
                  title="Cab Type Distribution")
    st.plotly_chart(fig2)

else:
    st.info("Download template → Fill data → Upload to view dashboard.")info("Download the template → Fill data → Upload to see analytics.")
