import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Analytics & Insights",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Analytics & Insights")

st.markdown("Analyze supplier performance, transport, routes and shipment delays.")

df = pd.read_csv(r"D:\Data science project\Smart Supply Chain Distruption prediction platform\Prediction_Result.csv")


df["Shipment_Date"] = pd.to_datetime(df["Shipment_Date"])



st.sidebar.header("🔎 Filters")




supplier = st.sidebar.selectbox(
    "Supplier",
    ["All"] + sorted(df["Supplier_Name"].dropna().unique().tolist())
)



transport_mapping = {
    0: "Road",
    1: "Rail",
    2: "Air",
    3: "Sea"
}

df["Transport_Mode"] = df["Transport_Mode"].replace(transport_mapping)



transport = st.sidebar.selectbox(
    "Transport Mode",
    ["All"] + sorted(df["Transport_Mode"].dropna().unique().tolist())
)



start_date = st.sidebar.date_input(
    "Start Date",
    df["Shipment_Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Shipment_Date"].max()
)



#apply filters #
filtered_df = df.copy()

if supplier != "All":
    filtered_df = filtered_df[
        filtered_df["Supplier_Name"] == supplier
    ]
    
    
if transport != "All":
    filtered_df = filtered_df[
        filtered_df["Transport_Mode"] == transport
    ]
    
    
filtered_df = filtered_df[
    (filtered_df["Shipment_Date"] >= pd.to_datetime(start_date))
    &
    (filtered_df["Shipment_Date"] <= pd.to_datetime(end_date))
]      
    
 # KPI Cards#   
    
st.subheader("📊 Key Performance Indicators")
    
total_shipments = len(filtered_df)

total_delay = filtered_df["Predicted_Delay"].sum()

average_delay = filtered_df["Delay_Hours"].mean()

transport_cost = filtered_df["Delivery_Cost"].sum()


#Display cards#

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Shipments",
        total_shipments
    )

with col2:
    st.metric(
        "Total Delay",
        round(total_delay,2)
    )

with col3:
    st.metric(
        "Average Delay Hours",
        round(average_delay,2)
    )

with col4:
    st.metric(
        "Transportation Cost",
        f"₹ {transport_cost:,.2f}"
    )
    
    
    
    st.subheader("📋 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# Supplier Analysis Heading#

st.markdown("---")
st.subheader("🏭 Supplier Analysis")  
    
# Average Delay by Supplier # 

supplier_delay = (
    filtered_df
    .groupby("Supplier_Name", as_index=False)["Delay_Hours"]
    .mean()
    .sort_values("Delay_Hours", ascending=False)
)


# Supplier Delay Chart #


fig_supplier_delay = px.bar(
    supplier_delay,
    x="Supplier_Name",
    y="Delay_Hours",
    color="Delay_Hours",
    title="Average Delay Hours by Supplier",
    text_auto=".2f"
)

fig_supplier_delay.update_layout(
    xaxis_title="Supplier",
    yaxis_title="Average Delay Hours",
    height=500
)

st.plotly_chart(
    fig_supplier_delay,
    use_container_width=True
)
 
 # Transportation Cost by Supplier #
 
supplier_cost = (
    filtered_df
    .groupby("Supplier_Name", as_index=False)["Delivery_Cost"]
    .sum()
    .sort_values("Delivery_Cost", ascending=False)
)
 
 
 
 
#Supplier Cost Chart#
 
fig_supplier_cost = px.bar(
    supplier_cost,
    x="Supplier_Name",
    y="Delivery_Cost",
    color="Delivery_Cost",
    title="Transportation Cost by Supplier",
    text_auto=True
)

fig_supplier_cost.update_layout(
    xaxis_title="Supplier",
    yaxis_title="Transportation Cost",
    height=500
)

st.plotly_chart(
    fig_supplier_cost,
    use_container_width=True
)



 # Top Suppliers Table# 
st.subheader("🏆 Top Suppliers")

top_supplier = supplier_delay.sort_values(
    "Delay_Hours"
).head(10)

st.dataframe(
    top_supplier,
    use_container_width=True,
    hide_index=True
)
 
 
 
 #Route Analysis#
st.markdown("---")
st.subheader("🏢 Route Analysis")


# Create Route Column #



# Average Delay by Route#



warehouse_delay = (
    filtered_df
    .groupby("Warehouse_City", as_index=False)["Delay_Hours"]
    .mean()
    .sort_values("Delay_Hours", ascending=False)
)


# Route Delay Chart#
fig = px.bar(
    warehouse_delay,
    x="Warehouse_City",
    y="Delay_Hours",
    color="Delay_Hours",
    title="Average Delay Hours by Warehouse",
    text_auto=".2f"
)

fig.update_layout(
    xaxis_title="Warehouse City",
    yaxis_title="Average Delay Hours",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Delivery Cost by Route#


warehouse_cost = (
    filtered_df
    .groupby("Warehouse_City", as_index=False)["Delivery_Cost"]
    .sum()
    .sort_values("Delivery_Cost", ascending=False)
)



# Route Cost Chart #
fig = px.bar(
    warehouse_cost,
    x="Warehouse_City",
    y="Delivery_Cost",
    color="Delivery_Cost",
    title="Transportation Cost by Warehouse",
    text_auto=True
)

fig.update_layout(
    xaxis_title="Warehouse City",
    yaxis_title="Transportation Cost",
    height=500
)

st.plotly_chart(fig, use_container_width=True)


# Warehouse Summary Table #

st.subheader("📋 Route Analysis Summary")

st.dataframe(
    warehouse_delay.head(10),
    use_container_width=True,
    hide_index=True
)



# Transport Mode Analysis #

st.markdown("---")
st.subheader("🚚 Transport Mode Analysis")


# Shipment Count by Transport Mode#
transport_shipments = (
    filtered_df
    .groupby("Transport_Mode", as_index=False)["Shipment_ID"]
    .count()
)

transport_shipments.rename(
    columns={"Shipment_ID": "Total Shipments"},
    inplace=True
)


# Shipment Chart# 


fig = px.bar(
    transport_shipments,
    x="Transport_Mode",
    y="Total Shipments",
    color="Transport_Mode",
    text_auto=True,
    title="Total Shipments by Transport Mode"
)

fig.update_layout(
    xaxis_title="Transport Mode",
    yaxis_title="Total Shipments",
    height=500
)

st.plotly_chart(fig, use_container_width=True)


# Average Delay by Transport Mode#
transport_delay = (
    filtered_df
    .groupby("Transport_Mode", as_index=False)["Delay_Hours"]
    .mean()
)


# Delay Chart # 

fig = px.bar(
    transport_delay,
    x="Transport_Mode",
    y="Delay_Hours",
    color="Delay_Hours",
    text_auto=".2f",
    title="Average Delay Hours by Transport Mode"
)

fig.update_layout(
    xaxis_title="Transport Mode",
    yaxis_title="Average Delay Hours",
    height=500
)

st.plotly_chart(fig, use_container_width=True)


# Transportation Cost by Mode #

transport_cost = (
    filtered_df
    .groupby("Transport_Mode", as_index=False)["Delivery_Cost"]
    .sum()
)


# Cost Chart #

fig = px.pie(
    transport_cost,
    names="Transport_Mode",
    values="Delivery_Cost",
    title="Transportation Cost Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# Delay Analysis # 
st.markdown("---")
st.subheader("⏳ Delay Analysis")

# Shipment Trend # 
shipment_trend = (
    filtered_df
    .groupby("Shipment_Date", as_index=False)["Shipment_ID"]
    .count()
)

shipment_trend.rename(
    columns={"Shipment_ID": "Total Shipments"},
    inplace=True
)


# Shipment Trend Chart # 
fig = px.line(
    shipment_trend,
    x="Shipment_Date",
    y="Total Shipments",
    markers=True,
    title="Shipment Trend"
)

fig.update_layout(
    xaxis_title="Shipment Date",
    yaxis_title="Total Shipments",
    height=500
)

st.plotly_chart(fig, use_container_width=True)


# Delay Trend # 
delay_trend = (
    filtered_df
    .groupby("Shipment_Date", as_index=False)["Delay_Hours"]
    .mean()
)

# Delay Trend Chart # 
fig = px.line(
    delay_trend,
    x="Shipment_Date",
    y="Delay_Hours",
    markers=True,
    title="Average Delay Trend"
)

fig.update_layout(
    xaxis_title="Shipment Date",
    yaxis_title="Average Delay Hours",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Delay Distribution
fig = px.histogram(
    filtered_df,
    x="Delay_Hours",
    nbins=25,
    title="Delay Hours Distribution"
)

fig.update_layout(
    xaxis_title="Delay Hours",
    yaxis_title="Frequency",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Delay by Weather # 
weather_delay = (
    filtered_df
    .groupby("Weather_Condition", as_index=False)["Delay_Hours"]
    .mean()
)

# Weather Chart # 
fig = px.bar(
    weather_delay,
    x="Weather_Condition",
    y="Delay_Hours",
    color="Delay_Hours",
    text_auto=".2f",
    title="Average Delay by Weather Condition"
)

fig.update_layout(
    xaxis_title="Weather Condition",
    yaxis_title="Average Delay Hours",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Delay by Traffic Level #
traffic_delay = (
    filtered_df
    .groupby("Traffic_Level", as_index=False)["Delay_Hours"]
    .mean()
)

# Traffic Chart #
fig = px.bar(
    traffic_delay,
    x="Traffic_Level",
    y="Delay_Hours",
    color="Delay_Hours",
    text_auto=".2f",
    title="Average Delay by Traffic Level"
)

fig.update_layout(
    xaxis_title="Traffic Level",
    yaxis_title="Average Delay Hours",
    height=500
)

st.plotly_chart(fig, use_container_width=True)


# Executive Summary #


st.markdown("---")
st.subheader("📋 Executive Summary")

# KPI Values
total_shipments = len(filtered_df)
average_delay = filtered_df["Delay_Hours"].mean()
total_transport_cost = filtered_df["Delivery_Cost"].sum()
avg_supplier = filtered_df["Supplier_Rating"].mean()

col1, col2 = st.columns(2)

with col1:

    st.info(
        f"""
### Shipment Summary

- Total Shipments : **{total_shipments}**

- Average Delay : **{average_delay:.2f} Hours**

- Total Transportation Cost : **₹ {total_transport_cost:,.2f}**
"""
    )

with col2:

    st.success(
        f"""
### Supplier Summary

- Average Supplier Rating : **{avg_supplier:.2f}**

- Total Suppliers : **{filtered_df['Supplier_Name'].nunique()}**

- Total Warehouses : **{filtered_df['Warehouse_City'].nunique()}**
"""
    )
    
    
    
    