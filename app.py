import streamlit as st
import requests
import pandas as pd
from datetime import datetime
st.set_page_config(page_title="Taxi Fare Prediction", layout="wide")
st.title('Taxi Fare Prediction')
st.markdown("""
Predict your taxi fare using our machine learning API!
""")
st.write("---")
col1, col2 = st.columns(2)
with col1:
    st.header("Enter Ride Details!")
    ride_date = st.date_input("Date", value=datetime.now())
    ride_time = st.time_input("Time", value=datetime.now())
    st.subheader("Pickup Location")
    pickup_lat = st.number_input("Pickup Latitude", value=40.7128, format="%.6f")
    pickup_lon = st.number_input("Pickup Longitude", value=-74.0060, format="%.6f")
    st.subheader("Dropoff Location")
    dropoff_lat = st.number_input("Dropoff Latitude", value=40.7306, format="%.6f")
    dropoff_lon = st.number_input("Dropoff Longitude", value=-73.9352, format="%.6f")
    passenger_count = st.number_input("Passenger Count", min_value=1, max_value=8, value=1)
    predict_button = st.button("Predict Fare")
with col2:
    st.header("Ride Map")
    map_data = pd.DataFrame({
        'lat': [pickup_lat, dropoff_lat],
        'lon': [pickup_lon, dropoff_lon],
    })
    st.map(map_data, zoom=12)
if predict_button:
    params = {
        "pickup_datetime": f"{ride_date} {ride_time}",
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passenger_count
    }
    api_url = "https://taxifare.lewagon.ai/predict"
    with st.spinner("Calculating fare prediction..."):
        try:
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                prediction = response.json().get("fare", 0)
                st.success(f"### Predicted Fare: ${prediction:.2f}")
                st.write("#### Parameters used:")
                st.json(params)
            else:
                st.error("Failed to get prediction. API returned status code: " + str(response.status_code))
        except requests.exceptions.RequestException as e:
            st.error(f"Error making API request: {e}")
st.write("---")
## Finally, we can display the prediction to the user
