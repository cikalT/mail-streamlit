import streamlit as st
import requests
from datetime import datetime
import toml

tokens =  st.secrets["TOKENS"]
namespaces = st.secrets["NAMESPACES"]

response = requests.get(f"https://api.testmail.app/api/json?apikey={tokens}&namespace={namespaces}&pretty=true")

print("this is the res", response)
data = response.json()

st.set_page_config(layout="wide")

st.header('EMAIL TESTING', divider='rainbow')
st.subheader('How to use:')
st.caption(f'{namespaces}.{{anything}}@inbox.testmail.app')

for email in data["emails"]:
    st.write(f"From: {email['from']}")
    st.write(f"To: {email['to']}")
    st.write(f"Subject: {email['subject']}")
    
    date_str = datetime.utcfromtimestamp(email['date'] / 1000).strftime('%d/%m/%Y')
    st.write(f"Date: {date_str}")
    st.components.v1.html(email['html'], height=1000, scrolling=True)
    
    st.write('---')