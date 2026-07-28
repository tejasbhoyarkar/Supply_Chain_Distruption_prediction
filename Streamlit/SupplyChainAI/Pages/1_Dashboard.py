import streamlit as st
import pandas as pd

# -----------------------------
# Page Title
# -----------------------------
st.title("📊 Dashboard Overview")

# -----------------------------
# Read CSV
# -----------------------------
df = pd.read_csv("Prediction_Result.csv")

# -----------------------------
# KPI Calculations
# -----------------------------
total_shipments = len(df)

total_delays = df["Predicted_Delay"].sum()

average_delay_hours = df["Delay_Hours"].mean()

total_transportation_cost = df["Delivery_Cost"].sum()

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Shipments", total_shipments)

with col2:
    st.metric("Total Delays", round(total_delays, 2))

with col3:
    st.metric("Total Transportation Cost", f"₹ {total_transportation_cost:,.2f}")

with col4:
    st.metric("Average Delay Hours", round(average_delay_hours, 2))
    
    
    

import plotly.express as px

shipment_trend = (
    df.groupby("Shipment_Date")
      .size()
      .reset_index(name="Total Shipments")
)

fig = px.line(
    shipment_trend,
    x="Shipment_Date",
    y="Total Shipments",
    title="Shipment Trend",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)



# ==============================
# Delay Trend
# ==============================

delay_trend = (
    df.groupby("Shipment_Date")["Delay_Hours"]
      .mean()
      .reset_index()
)

fig = px.line(
    delay_trend,
    x="Shipment_Date",
    y="Delay_Hours",
    title="Average Delay Hours Trend",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)



# ==============================
# Supplier Performance Analysis
# ==============================

# Supplier-wise Average Delay Hours
supplier_performance = (
    df.groupby("Supplier_Name", as_index=False)
      .agg({
          "Delay_Hours": "mean"
      })
      .sort_values(by="Delay_Hours", ascending=True)
)

# Create Bar Chart
fig = px.bar(
    supplier_performance,
    x="Supplier_Name",
    y="Delay_Hours",
    title="Supplier Performance (Average Delay Hours)",
    text_auto=".2f",
    color="Delay_Hours"
)

# Improve Layout
fig.update_layout(
    xaxis_title=" Supplier Name",
    yaxis_title="Average Delay Hours",
    title_x=0.,
    template="plotly_white",
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)

