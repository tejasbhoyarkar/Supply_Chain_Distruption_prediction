# ==========================================================
# Import Libraries
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib

from database import get_connection
from datetime import datetime

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Disruption Prediction",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Supply Chain Disruption Prediction")
st.markdown(
    """
Predict shipment delay and disruption risk using Machine Learning.
"""
)

# ==========================================================
# Load Master Dataset
# ==========================================================

@st.cache_data
def load_dataset():

    return pd.read_csv("Prediction_Result.csv")


master_df = load_dataset()

# ==========================================================
# Supplier & Warehouse Lists
# ==========================================================

supplier_list = sorted(
    master_df["Supplier_Name"].dropna().unique().tolist()
)

warehouse_list = sorted(
    master_df["Warehouse_City"].dropna().unique().tolist()
)

# ==========================================================
# Load ML Models
# ==========================================================

@st.cache_resource
def load_models():

    delay_model = joblib.load(r"D:\Data science project\Smart Supply Chain Distruption prediction platform\delay_prediction_model.pkl")

    risk_model = joblib.load(r"D:\Data science project\Smart Supply Chain Distruption prediction platform\disruption_classifier.pkl")

    return delay_model, risk_model


delay_model, risk_model = load_models()

# ==========================================================
# Save Prediction into MySQL
# ==========================================================

def save_prediction(
    supplier_name,
    warehouse_city,
    transport_mode,
    predicted_delay,
    risk_level,
    confidence_score,
    suggested_action
):

    try:

        connection = get_connection()

        cursor = connection.cursor()

        sql = """
        INSERT INTO Prediction_History
        (
            Prediction_Time,
            Supplier_Name,
            Warehouse_City,
            Transport_Mode,
            Predicted_Delay,
            Risk_Level,
            Confidence_Score,
            Suggested_Action
        )

        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s
        )
        """

        values = (

            datetime.now(),

            supplier_name,

            warehouse_city,

            transport_mode,

            float(predicted_delay),

            risk_level,

            float(confidence_score),

            suggested_action

        )

        cursor.execute(sql, values)

        connection.commit()

        cursor.close()

        connection.close()

    except Exception as e:

        st.error(f"MySQL Error : {e}")


# ==========================================================
# Shipment Details
# ==========================================================

st.markdown("---")
st.subheader("📦 Enter Shipment Details")

col1, col2 = st.columns(2)

# ==========================================================
# Left Column
# ==========================================================

with col1:

    supplier_name = st.selectbox(
        "Supplier Name",
        supplier_list
    )

    warehouse_city = st.selectbox(
        "Warehouse City",
        warehouse_list
    )

    supplier_rating = st.slider(
        "Supplier Rating",
        min_value=1.0,
        max_value=5.0,
        value=3.5,
        step=0.1
    )

    warehouse_capacity = st.number_input(
        "Warehouse Capacity",
        min_value=0,
        max_value=10000,
        value=500,
        step=50
    )

    delivery_time = st.number_input(
        "Delivery Time (Hours)",
        min_value=1,
        max_value=500,
        value=24,
        step=1
    )

    route_distance = st.number_input(
        "Route Distance (KM)",
        min_value=1,
        max_value=5000,
        value=500,
        step=10
    )

    fuel_cost = st.number_input(
        "Fuel Cost (₹)",
        min_value=0.0,
        value=95.0,
        step=1.0
    )

    delivery_cost = st.number_input(
        "Transportation Cost (₹)",
        min_value=0.0,
        value=5000.0,
        step=100.0
    )

# ==========================================================
# Right Column
# ==========================================================

with col2:

    transport_mode = st.selectbox(
        "Transport Mode",
        [
            "Road",
            "Rail",
            "Air",
            "Sea"
        ]
    )

    weather = st.selectbox(
        "Weather Condition",
        [
            "Clear",
            "Fog",
            "Rain",
            "Storm",
            "Snow"
        ]
    )

    traffic = st.selectbox(
        "Traffic Level",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    port_congestion = st.selectbox(
        "Port Congestion",
        [
            "No",
            "Yes"
        ]
    )

    holiday = st.selectbox(
        "Holiday",
        [
            "No",
            "Yes"
        ]
    )

    customer_priority = st.selectbox(
        "Customer Priority",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

# ==========================================================
# Predict Button
# ==========================================================

st.markdown("")

predict = st.button(
    "🚀 Predict Disruption",
    type="primary",
    use_container_width=True
)
# ==========================================================
# Manual Encoding
# ==========================================================

transport_mapping = {
    "Road": 0,
    "Rail": 1,
    "Air": 2,
    "Sea": 3
}

weather_mapping = {
    "Clear": 0,
    "Fog": 1,
    "Rain": 2,
    "Storm": 3,
    "Snow": 4
}

traffic_mapping = {
    "Low": 0,
    "Medium": 1,
    "High": 2
}

priority_mapping = {
    "Low": 0,
    "Medium": 1,
    "High": 2
}

port_mapping = {
    "No": 0,
    "Yes": 1
}

holiday_mapping = {
    "No": 0,
    "Yes": 1
}

# ==========================================================
# Prediction Start
# ==========================================================

if predict:

    # -----------------------------------------
    # Validation
    # -----------------------------------------

    if supplier_name == "":
        st.error("Please select Supplier Name.")
        st.stop()

    if warehouse_city == "":
        st.error("Please select Warehouse City.")
        st.stop()

    # -----------------------------------------
    # Encode Categorical Values
    # -----------------------------------------

    transport_value = transport_mapping[transport_mode]

    weather_value = weather_mapping[weather]

    traffic_value = traffic_mapping[traffic]

    priority_value = priority_mapping[customer_priority]

    port_value = port_mapping[port_congestion]

    holiday_value = holiday_mapping[holiday]

    # -----------------------------------------
    # Delay Prediction Input
    # -----------------------------------------

    input_data = np.array([[
        supplier_rating,
        warehouse_capacity,
        delivery_time,
        transport_value,
        route_distance,
        fuel_cost,
        weather_value,
        traffic_value,
        port_value,
        holiday_value,
        delivery_cost,
        priority_value
    ]])

    # -----------------------------------------
    # Delay Prediction
    # -----------------------------------------

    predicted_delay = float(
        delay_model.predict(input_data)[0]
    )

    # -----------------------------------------
    # Risk Model Input
    # -----------------------------------------

    risk_input = np.array([[
        supplier_rating,
        warehouse_capacity,
        delivery_time,
        transport_value,
        route_distance,
        fuel_cost,
        weather_value,
        traffic_value,
        port_value,
        holiday_value,
        delivery_cost,
        priority_value,
        predicted_delay
    ]])

        # ==========================================================
    # Risk Prediction
    # ==========================================================

    disruption_prediction = risk_model.predict(risk_input)[0]

    # ==========================================================
    # Confidence Score
    # ==========================================================

    try:

        confidence_score = float(
            np.max(
                risk_model.predict_proba(risk_input)
            ) * 100
        )

    except Exception:

        confidence_score = 95.00

    # ==========================================================
    # Risk Level
    # ==========================================================

    if disruption_prediction == 0:

        risk_level = "🟢 Low Risk"

    elif disruption_prediction == 1:

        risk_level = "🟡 Medium Risk"

    else:

        risk_level = "🔴 High Risk"

    # ==========================================================
    # Suggested Action
    # ==========================================================

    if predicted_delay <= 5:

        suggested_action = (
            "Shipment is on schedule."
        )

    elif predicted_delay <= 15:

        suggested_action = (
            "Monitor shipment and inform customer."
        )

    else:

        suggested_action = (
            "Use alternate route or faster transport."
        )

    # ==========================================================
    # Save Prediction to MySQL
    # ==========================================================

    save_prediction(

        supplier_name=supplier_name,

        warehouse_city=warehouse_city,

        transport_mode=transport_mode,

        predicted_delay=predicted_delay,

        risk_level=risk_level,

        confidence_score=confidence_score,

        suggested_action=suggested_action

    )

    # ==========================================================
    # Success Message
    # ==========================================================

    st.success("Prediction Completed Successfully!")

    # ==========================================================
    # KPI Cards
    # ==========================================================

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Predicted Delay",

            f"{predicted_delay:.2f} Hours"

        )

    with col2:

        st.metric(

            "Risk Level",

            risk_level

        )

    with col3:

        st.metric(

            "Confidence Score",

            f"{confidence_score:.2f}%"

        )

    # ==========================================================
    # Suggested Action
    # ==========================================================

    st.markdown("---")

    st.subheader("📌 Suggested Action")

    st.info(suggested_action)

    # ==========================================================
    # Prediction Summary
    # ==========================================================

    st.markdown("---")

    st.subheader("📋 Prediction Summary")

    summary = pd.DataFrame({

        "Supplier Name":[supplier_name],

        "Warehouse City":[warehouse_city],

        "Transport Mode":[transport_mode],

        "Predicted Delay (Hours)":[round(predicted_delay,2)],

        "Risk Level":[risk_level],

        "Confidence Score (%)":[round(confidence_score,2)],

        "Suggested Action":[suggested_action]

    })

    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )

    # ==========================================================
    # Download Prediction Report
    # ==========================================================

    csv = summary.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="📥 Download Prediction Report",

        data=csv,

        file_name="Prediction_Report.csv",

        mime="text/csv"

    )


# ==========================================================
# Prediction Analysis + AI Recommendation
# ==========================================================

if predict:

    # Delay Prediction
    predicted_delay = float(delay_model.predict(input_data)[0])

    # Risk Prediction
    disruption_prediction = risk_model.predict(risk_input)[0]

    # Confidence Score
    try:
        confidence_score = float(
            risk_model.predict_proba(risk_input).max() * 100
        )
    except:
        confidence_score = 95.0

    # Risk Level
    if disruption_prediction == 0:
        risk_level = "🟢 Low Risk"
    elif disruption_prediction == 1:
        risk_level = "🟡 Medium Risk"
    else:
        risk_level = "🔴 High Risk"

    # Suggested Action
    if predicted_delay <= 5:
        suggested_action = "Shipment is on schedule."
    elif predicted_delay <= 15:
        suggested_action = "Monitor shipment and inform customer."
    else:
        suggested_action = "Use alternate route or faster transport."

    # ✅ Session State yahin save karo
    st.session_state["predicted_delay"] = predicted_delay
    st.session_state["risk_level"] = risk_level
    st.session_state["confidence_score"] = confidence_score
    st.session_state["suggested_action"] = suggested_action
    # ------------------------------
    # AI Recommendation
    # ------------------------------

    st.markdown("---")
    st.subheader("🤖 AI Recommendation")

    if risk_level == "🟢 Low Risk":

        st.success("""
Shipment is expected to arrive on time.

Recommended Action

• Continue normal operations

• Track shipment periodically

• No urgent action required
""")

    elif risk_level == "🟡 Medium Risk":

        st.warning("""
Shipment may experience delay.

Recommended Action

• Notify customer

• Monitor shipment

• Prepare backup transport
""")

    else:

        st.error("""
High disruption risk detected.

Recommended Action

• Use alternate route

• Inform warehouse

• Prioritize shipment

• Use faster transport
""")

# ==========================================================
# Last 5 Predictions
# ==========================================================

st.markdown("---")
st.subheader("🕒 Last 5 Predictions")

try:

    connection = get_connection()

    query = """
    SELECT
        Prediction_Time,
        Supplier_Name,
        Warehouse_City,
        Transport_Mode,
        Predicted_Delay,
        Risk_Level,
        Confidence_Score
    FROM Prediction_History
    ORDER BY Prediction_Time DESC
    LIMIT 5
    """

    history_df = pd.read_sql(query, connection)

    connection.close()

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

except Exception as e:

    st.warning("Prediction History not available.")

    st.write(e)





    # ==========================================================
# Footer
# ==========================================================

st.markdown("---")

st.caption(
    """
Smart Supply Chain Disruption Prediction Platform

Developed using

Python • Machine Learning • Streamlit • MySQL • Plotly
"""
)


