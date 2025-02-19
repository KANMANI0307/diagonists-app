import streamlit as st
import requests

# Backend API URL (Change this if your Django app is hosted)
BASE_URL = "http://127.0.0.1:8000"

# Page title
st.title("Doctor Appointment Booking")

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
    
    from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('qualification', models.CharField(max_length=256)),
                ('specialization', models.CharField(choices=[('Allergy & Clinical Immunology', 'Allergy & Clinical Immunology'), ('Anesthesiologists', 'Anesthesiologists'), ('Blood Screening', 'Blood Screening'), ('Cardiology', 'Cardiology'), ('Dentistry', 'Dentistry'), ('ENT Specialists', 'ENT Specialists'), ('Eye Care', 'Eye Care'), ('Gastroenterologists', 'Gastroenterologists'), ('Neuroanatomy', 'Neuroanatomy'), ('Oncologists', 'Oncologists'), ('Pediatricians', 'Pediatricians'), ('Physical Therapy', 'Physical Therapy')], max_length=100)),
                ('hospitalName', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Doctor',
            },
        ),
        migrations.CreateModel(
            name='Timeslots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetimeslot', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointment.doctor')),
            ],
            options={
                'verbose_name_plural': 'Timeslots',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meetingId', models.CharField(max_length=50)),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointment.timeslots')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
