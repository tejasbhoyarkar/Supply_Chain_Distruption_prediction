# ============================================================
# Prediction History
# Smart Supply Chain Disruption Prediction Platform
# ============================================================

import streamlit as st
import pandas as pd
from database import get_connection

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Prediction History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Prediction History")
st.markdown("View all prediction records stored in the MySQL database.")

# ============================================================
# Refresh Button
# ============================================================

col1, col2 = st.columns([8, 1])

with col2:
    if st.button("🔄 Refresh"):
        st.rerun()

# ============================================================
# Load Data From MySQL
# ============================================================

try:

    connection = get_connection()

    query = """
    SELECT *
    FROM Prediction_History
    ORDER BY Prediction_Time DESC
    """

    df = pd.read_sql(query, connection)

    connection.close()

except Exception as e:

    st.error(f"MySQL Error : {e}")
    st.stop()

# ============================================================
# Check Empty Table
# ============================================================

if df.empty:

    st.warning("⚠ No Prediction History Found.")
    st.info(
        "Go to the Disruption Prediction page and generate a prediction first."
    )
    st.stop()

# ============================================================
# Format Date
# ============================================================

df["Prediction_Time"] = pd.to_datetime(
    df["Prediction_Time"],
    errors="coerce"
)

df = df.sort_values(
    by="Prediction_Time",
    ascending=False
)

# ============================================================
# Search
# ============================================================

search = st.text_input(
    "🔍 Search Supplier / Warehouse"
)

if search:

    df = df[
        df["Supplier_Name"].astype(str).str.contains(search, case=False)
        |
        df["Warehouse_City"].astype(str).str.contains(search, case=False)
    ]

# ============================================================
# Date Filter
# ============================================================

col1, col2 = st.columns(2)

with col1:

    start_date = st.date_input(
        "From Date",
        df["Prediction_Time"].min().date()
    )

with col2:

    end_date = st.date_input(
        "To Date",
        df["Prediction_Time"].max().date()
    )

df = df[
    (df["Prediction_Time"].dt.date >= start_date)
    &
    (df["Prediction_Time"].dt.date <= end_date)
]

# ============================================================
# KPI Cards
# ============================================================

st.markdown("## 📊 Prediction Summary")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Total Predictions", len(df))

with k2:
    st.metric(
        "Average Delay",
        f"{df['Predicted_Delay'].mean():.2f} Hours"
    )

with k3:
    st.metric(
        "Average Confidence",
        f"{df['Confidence_Score'].mean():.2f}%"
    )

with k4:
    st.metric(
        "High Risk Shipments",
        len(df[df["Risk_Level"].str.contains("High", case=False)])
    )

# ============================================================
# Prediction History Table
# ============================================================

st.markdown("## 📋 Prediction Records")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# Download Report
# ============================================================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Prediction Report",
    data=csv,
    file_name="Prediction_History.csv",
    mime="text/csv"
)

# ============================================================
# Footer
# ============================================================

st.markdown("---")

st.caption(
    "Smart Supply Chain Disruption Prediction Platform | "
    "Python • Streamlit • Machine Learning • MySQL"
)