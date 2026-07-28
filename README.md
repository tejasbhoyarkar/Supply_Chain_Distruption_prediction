# Supply_Chain_Distruption_prediction

🚚 Smart Supply Chain Delay Prediction & Analytics
📌 Project Overview

This project is an AI-powered Supply Chain Analytics and Shipment Delay Prediction System developed using Python, Machine Learning, SQL, and Streamlit. The objective is to analyze supply chain operations, identify shipment delay patterns, and predict the expected shipment delay based on operational factors.

The project provides an interactive dashboard for business users to monitor shipment performance, explore supply chain data, and make data-driven decisions.

🎯 Objectives
Analyze supply chain shipment data.
Identify factors affecting shipment delays.
Build a Machine Learning model for delay prediction.
Visualize KPIs and business insights.
Deploy the solution using Streamlit.

🛠 Technologies Used
Category	Technology
Programming	Python
Database	MYSQL / SQL
Data Analysis	Pandas, NumPy
Visualization	Matplotlib
Machine Learning	Scikit-learn
Deployment	Streamlit
Model Saving	Joblib


📂 Project Structure
Supply_Chain/
│
├── data/
│   └── supply_chain_dataset.csv
│
├── Streamlit_Supply_Chain.py
├── Machine_Learning.ipynb
├── cleaned_project_jupyter.ipynb
├── Logging_Monitoring.ipynb
├── SQL_Integration.sqbpro
├── sql_new.sqbpro
├── README.md
├── requirements.txt
└── .gitignore




📊 Machine Learning Workflow
Data Collection
        │
        ▼
Data Cleaning
        │
        ▼
Exploratory Data Analysis (EDA)
        │
        ▼
Feature Engineering
        │
        ▼
Data Preprocessing
        │
        ▼
Model Training
        │
        ▼
Model Evaluation
        │
        ▼
Prediction
        │
        ▼
Streamlit Deployment



📈 Dataset Features

The Machine Learning model uses the following features:

Supplier Rating
Transport Mode
Weather Condition
Traffic Level
Route Distance (km)
Target Variable
Expected Shipment Delay Hours
🤖 Machine Learning Model
Input Features
Supplier Rating
Route Distance
Transport Mode
Weather Condition
Traffic Level
Output

Predicted Shipment Delay (Hours)

📸 Streamlit Application Modules
🏠 Home
Project Introduction
Dataset Information
KPI Cards
Workflow Overview


📊 Dashboard

Displays important business metrics including:

Total Shipments
Average Delay Hours
Transportation Cost
Shipment Trends
Delivery Performance
🔍 Shipment Explorer

Users can filter shipment records using:

Supplier
Warehouse
Transport Mode
🤖 Delay Prediction

Users enter:

Supplier Rating
Route Distance
Transport Mode
Weather Condition
Traffic Level

The trained Machine Learning model predicts:

✅ Expected Shipment Delay Hours


📈 Analytics

Provides visual analysis including:

Supplier Performance
Transportation Analysis
Delay Distribution
Weather Impact
Traffic Analysis
Business Insights

📊 Key Performance Indicators (KPIs)
Total Shipments
Average Shipment Delay
Maximum Delay
Transportation Cost
On-Time Delivery Percentage
Average Supplier Rating

📈 Data Analysis Performed
Missing Value Handling
Duplicate Removal
Outlier Detection
Feature Encoding
Feature Scaling
Correlation Analysis
Data Visualization
Model Evaluation


📦 Installation
Clone Repository
git clone https://github.com/yourusername/Supply_Chain.git
Navigate to Project
cd Supply_Chain
Install Required Libraries
pip install -r requirements.txt
Run Streamlit App
streamlit run Streamlit_Supply_Chain.py
📦 Required Libraries
streamlit
pandas
numpy
matplotlib
scikit-learn
joblib
sqlite3

Install manually:

pip install streamlit pandas numpy matplotlib scikit-learn joblib
📊 Machine Learning Pipeline
Load Dataset
Clean Data
Handle Missing Values
Encode Categorical Features
Train-Test Split
Model Training
Model Evaluation
Save Model using Joblib
Deploy with Streamlit
📈 Business Benefits
Predict shipment delays before dispatch.
Improve logistics planning.
Reduce transportation costs.
Identify supplier performance issues.
Support data-driven decision-making.
Improve customer satisfaction through better delivery planning.
🎯 Future Enhancements
Real-Time Shipment Tracking
Route Optimization
Weather API Integration
Interactive Maps
User Authentication
Cloud Deployment
Automated Model Retraining
Power BI Dashboard Integration
Email Notifications for Delayed Shipments
👨‍💻 Author

Tejas Bhoyarkar

B.Tech Electronics & Telecommunication Engineering

Priyadarshini College of Engineering, Nagpur

Specialization: Data Analytics | Data Science | Machine Learning



