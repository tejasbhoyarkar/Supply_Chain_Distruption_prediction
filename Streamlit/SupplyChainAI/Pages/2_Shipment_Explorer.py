import streamlit as st
import pandas as pd

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Shipment Explorer",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Shipment Explorer")
st.markdown("Search and filter shipment details.")

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
df = pd.read_csv("Prediction_Result.csv")

# Convert Shipment_Date to Date format
df["Shipment_Date"] = pd.to_datetime(df["Shipment_Date"])




transport_map = {
    0: "Road",
    1: "Rail",
    2: "Air",
    3: "Sea"
}

priority_map = {
    0: "Low",
    1: "Medium",
    2: "High"
}
if df["Transport_Mode"].dtype != object:
    df["Transport_Mode"] = df["Transport_Mode"].replace(transport_map)

if df["Customer_Priority"].dtype != object:
    df["Customer_Priority"] = df["Customer_Priority"].replace(priority_map)
# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("🔍 Filters")

supplier = st.sidebar.selectbox(
    "Supplier",
    ["All"] + sorted(df["Supplier_Name"].unique().tolist())
)

warehouse = st.sidebar.selectbox(
    "Warehouse",
    ["All"] + sorted(df["Warehouse_City"].unique().tolist())
)

transport = st.sidebar.selectbox(
    "Transport Mode",
    ["All"] + sorted(df["Transport_Mode"].unique().tolist())
)

priority = st.sidebar.selectbox(
    "Customer Priority",
    ["All"] + sorted(df["Customer_Priority"].unique().tolist())
)

# -------------------------------------------------
# Shipment ID Search
# -------------------------------------------------
search = st.sidebar.text_input("Search Shipment ID")

# -------------------------------------------------
# Apply Filters
# -------------------------------------------------
filtered_df = df.copy()

if supplier != "All":
    filtered_df = filtered_df[
        filtered_df["Supplier_Name"] == supplier
    ]

if warehouse != "All":
    filtered_df = filtered_df[
        filtered_df["Warehouse_City"] == warehouse
    ]

if transport != "All":
    filtered_df = filtered_df[
        filtered_df["Transport_Mode"] == transport
    ]

if priority != "All":
    filtered_df = filtered_df[
        filtered_df["Customer_Priority"] == priority
    ]

if search != "":
    filtered_df = filtered_df[
        filtered_df["Shipment_ID"]
        .astype(str)
        .str.contains(search, case=False, na=False)
    ]

# -------------------------------------------------
# Summary Cards
# -------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Shipments", len(filtered_df))

with col2:
    st.metric(
        "Average Delay",
        f"{filtered_df['Delay_Hours'].mean():.2f} Hours"
    )

with col3:
    st.metric(
        "Average Delivery Cost",
        f"₹ {filtered_df['Delivery_Cost'].mean():,.2f}"
    )

with col4:
    st.metric(
        "Total Delivery Cost",
        f"₹ {filtered_df['Delivery_Cost'].sum():,.2f}"
    )

# -------------------------------------------------
# Display Data
# -------------------------------------------------
st.subheader("Shipment Details")

display_columns = [
    "Shipment_ID",
    "Shipment_Date",
    "Supplier_Name",
    "Warehouse_City",
    "Transport_Mode",
    "Delay_Hours",
    "Delivery_Cost",
    "Predicted_Delay",
    "Customer_Priority",
    "Disruption_Status"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------
# Total Records
# -------------------------------------------------
st.success(f"Total Records Found : {len(filtered_df)}")

# -------------------------------------------------
# Download Button
# -------------------------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="Filtered_Shipments.csv",
    mime="text/csv"
)