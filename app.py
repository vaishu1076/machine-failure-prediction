import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Machine Failure Prediction",
    page_icon="⚙️",
    layout="centered"
)

# Load saved model and preprocessing pipeline
model = joblib.load("gradient_boosting_model.joblib")
pipeline = joblib.load("preprocessing_pipeline.joblib")

st.title("⚙️ Machine Failure Prediction")
st.write("Enter machine parameters to predict potential failure.")

machine_type = st.selectbox("Machine Type", ["L", "M", "H"])

air_temp = st.number_input(
    "Air Temperature (K)",
    min_value=250.0,
    max_value=350.0,
    value=300.0
)

process_temp = st.number_input(
    "Process Temperature (K)",
    min_value=250.0,
    max_value=400.0,
    value=310.0
)

rot_speed = st.number_input(
    "Rotational Speed (rpm)",
    min_value=0,
    max_value=10000,
    value=1500
)

torque = st.number_input(
    "Torque (Nm)",
    min_value=0.0,
    max_value=200.0,
    value=40.0
)

tool_wear = st.number_input(
    "Tool Wear (min)",
    min_value=0,
    max_value=500,
    value=100
)

if st.button("Predict Machine Failure"):

    input_data = pd.DataFrame([{
        "Type": machine_type,
        "Air temperature [K]": air_temp,
        "Process temperature [K]": process_temp,
        "Rotational speed [rpm]": rot_speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear
    }])

    transformed_data = pipeline.transform(input_data)
    prediction = model.predict(transformed_data)[0]

    if prediction == 1:
        st.error("⚠️ Machine Failure Predicted")
    else:
        st.success("✅ No Machine Failure Predicted")
