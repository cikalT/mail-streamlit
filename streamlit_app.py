import streamlit as st
import requests
from datetime import datetime


# Make a request to fetch the JSON data
response = requests.get("https://api.testmail.app/api/json?apikey=bfe23c1a-a2b4-49a6-95e5-4b39e27de424&namespace=84z4f&pretty=true")
data = response.json()

for email in data["emails"]:
    st.write(f"From: {email['from']}")
    st.write(f"To: {email['to']}")
    st.write(f"Subject: {email['subject']}")
    
    # Convert timestamp to Day/Month/Year format
    date_str = datetime.utcfromtimestamp(email['date'] / 1000).strftime('%d/%m/%Y')
    st.write(f"Date: {date_str}")
    
    st.components.v1.html(email['html'], height=500, scrolling=True)  # Render HTML content
    
    # Add a separator between emails
    st.write('---')