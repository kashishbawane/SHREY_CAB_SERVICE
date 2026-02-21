import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SHREY CAB SERVICES Dashboard",
                   page_icon="🚖",
                   layout="wide")

# ---------------- COMPANY HEADER ----------------
st.markdown("""
    <h1 style='text-align:center; color:#0A3D62;'>
    🚖 SHREY CAB SERVICES – Business Analytics Dashboard
    </h1>
""", unsafe_allow_html=True)

st.write("Manage bookings, revenue & analytics easily.")

# ---------------- CREATE BLANK EXCEL TEMPLATE ----------------
def create_template():
    data = {
        "Booking_ID": [],
        "Customer_Name": [],
        "City": [],
        "Cab_Type": [],
        "Trip_Date": [],
        "Fare_Amount": []
    }
    df = pd.DataFrame(data)
    return df

template_df = create_template()

# Convert to Excel
def convert_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Cab_Data')
    processed_data = output.getvalue()
    return processed_data

excel_file = convert_to_excel(template_df)

st.download_button(
    label="📥 Download Blank Excel Template",
    data=excel_file,
    file_name="SHREY_CAB_TEMPLATE.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.divider()

# ---------------- UPLOAD FILLED EXCEL ----------------
uploaded_file = st.file_uploader("📤 Upload Filled Excel File", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("📋 Uploaded Data")
    st.dataframe(df, use_container_width=True)

    # ---------------- KPI METRICS ----------------
    total_bookings = len(df)
    total_revenue = df["Fare_Amount"].sum()
    avg_fare = df["Fare_Amount"].mean()

    c1, c2, c3 = st.columns(3)

    c1.metric("🚖 Total Bookings", total_bookings)
    c2.metric("💰 Total Revenue", f"₹ {total_revenue}")
    c3.metric("📊 Average Fare", f"₹ {round(avg_fare,2)}")

    st.divider()

    # ---------------- PIE CHART 1: Revenue by City ----------------
    st.subheader("📊 Revenue Distribution by City")

    city_revenue = df.groupby("City")["Fare_Amount"].sum().reset_index()

    fig_city = px.pie(
        city_revenue,
        names="City",
        values="Fare_Amount",
        title="Revenue by City",
        hole=0.4
    )

    st.plotly_chart(fig_city)

    # ---------------- PIE CHART 2: Cab Type Distribution ----------------
    st.subheader("🚘 Cab Type Distribution")

    cab_count = df["Cab_Type"].value_counts().reset_index()
    cab_count.columns = ["Cab_Type", "Count"]

    fig_cab = px.pie(
        cab_count,
        names="Cab_Type",
        values="Count",
        title="Cab Type Usage",
        hole=0.4
    )

    st.plotly_chart(fig_cab)

    # ---------------- DAILY REVENUE LINE CHART ----------------
    st.subheader("📈 Daily Revenue Trend")

    df["Trip_Date"] = pd.to_datetime(df["Trip_Date"])
    daily_revenue = df.groupby("Trip_Date")["Fare_Amount"].sum().reset_index()

    fig_line = px.line(
        daily_revenue,
        x="Trip_Date",
        y="Fare_Amount",
        markers=True,
        title="Daily Revenue Trend"
    )

    st.plotly_chart(fig_line)

    st.success("✅ Dashboard Updated Successfully!")

else:
    st.info("Download the template → Fill data → Upload to see analytics.")
