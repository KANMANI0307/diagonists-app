import streamlit as st
import requests

st.little("contact form")

name = st.text_input("name")
email= st.text_input("email")
message = st.text_input("message")


if st.button("submit"):
    data ={
        "name":name,
        "email":email,
        "message":message
    }
    response = requests.post("http://127.0.0.1:8000/submit_form",json=data)
    if response.ststus_code ==200:
        st.success("form submitted successfully")

    else:
        st.error("error submitting form. please try again")
