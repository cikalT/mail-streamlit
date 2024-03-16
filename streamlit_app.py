import streamlit as st
import requests
from datetime import datetime

def get_email_data(tokens, namespaces, offset=0):
    response = requests.get(f"https://api.testmail.app/api/json?apikey={tokens}&namespace={namespaces}&pretty=true&limit=100&offset={offset}")
    return response.json()

tokens = st.secrets["TOKENS"]
namespaces = st.secrets["NAMESPACES"]

st.set_page_config(layout="wide")

st.header('EMAIL TESTING', divider='rainbow')
st.subheader('How to use:')
st.caption(f'{namespaces}.{{use anything in this section}}@inbox.testmail.app')

emails_by_recipient = {}

offset = 0
while True:
    data = get_email_data(tokens, namespaces, offset)
    for email in data["emails"]:
        recipient = email['to']
        if recipient not in emails_by_recipient:
            emails_by_recipient[recipient] = []
        emails_by_recipient[recipient].append(email)

    if len(data["emails"]) < 100:
        break
    else:
        offset += 100

left_column, right_column = st.columns([1, 3])

with left_column:
    selected_recipient_emails = None
    for recipient, emails in emails_by_recipient.items():
        recipient_button_label = f"To: {recipient} ({len(emails)} emails)"
        if st.button(recipient_button_label):
            selected_recipient_emails = emails

with right_column:
    if selected_recipient_emails is not None:
        for email in selected_recipient_emails:
            st.write(f"From: {email['from']}")
            st.write(f"To: {email['to']}")
            st.write(f"Subject: {email['subject']}")
            
            date_str = datetime.utcfromtimestamp(email['date'] / 1000).strftime('%d/%m/%Y')
            st.write(f"Date: {date_str}", divider='green')
            st.components.v1.html(email['html'], height=1000, scrolling=True)
            st.header('', divider='green')
