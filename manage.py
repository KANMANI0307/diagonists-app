import streamlit as st
import requests

# Backend API URL (Change if your Django app is hosted online)
BASE_URL = "http://127.0.0.1:8000"

# Page title
st.title("Doctor Appointment Booking System")

# Fetch doctors from Django API
st.subheader("Select a Doctor")
doctors_response = requests.get(f"{BASE_URL}/doctors/")

if doctors_response.status_code == 200:
    doctors = doctors_response.json()
    doctor_dict = {doc["name"]: doc["id"] for doc in doctors}
    selected_doctor = st.selectbox("Choose a doctor:", list(doctor_dict.keys()))

    # Fetch timeslots for selected doctor
    if selected_doctor:
        doctor_id = doctor_dict[selected_doctor]
        timeslots_response = requests.get(f"{BASE_URL}/timeslots/{doctor_id}/")
        
        if timeslots_response.status_code == 200:
            timeslots = timeslots_response.json()
            if timeslots:
                selected_timeslot = st.selectbox("Choose a timeslot:", [t["datetimeslot"] for t in timeslots])
                
                if st.button("Book Appointment"):
                    st.success(f"Appointment booked with Dr. {selected_doctor} at {selected_timeslot}")
            else:
                st.warning("No available timeslots.")
        else:
            st.error("Failed to fetch timeslots.")
else:
    st.error("Failed to fetch doctors.")
