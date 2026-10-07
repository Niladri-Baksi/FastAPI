import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("Insurance Premium Category Prediction")
st.markdown("Enter your details below:")

# User input fields
age = st.number_input("Age", min_value=1, max_value=120, value=30)
weight = st.number_input("Weight (in kgs)", min_value=1.0, value=65.0)
height = st.number_input("Height (in meters)", min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input("Annual Income (in LPA)", min_value=0.0, value=10.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox(
    "Occupation",
    options=[
        'student', 'retired', 'self_employed', 'business_owner',
        'private_job', 'unemployed', 'government_job'
    ]
)

if st.button("Predict Insurance Premium Category"):
    user_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=user_data)

        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Insurance Premium Category: **{result['predicted_premium_category']}**")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the API. Please ensure the FastAPI server is running on port 8000.")

    