import streamlit as st
import requests
from datetime import datetime, timezone

def get_email_data(tokens, namespaces, offset=0):
    response = requests.get(f"https://api.testmail.app/api/json?apikey={tokens}&namespace={namespaces}&pretty=true&limit=100&offset={offset}")
    return response.json()

tokens = st.secrets["TOKENS"]
namespaces = st.secrets["NAMESPACES"]
password = st.secrets["PASSWORD"]

st.set_page_config(layout="wide")
if "password_entered" not in st.session_state:
    st.session_state.password_entered = False

if not st.session_state.password_entered:
    user_password = st.text_input("Enter password:", type="password")

    
    if user_password == password:
        st.session_state.password_entered = True
    elif user_password != "":
        st.error("Incorrect password. Please try again.")

if st.session_state.password_entered:
    
    st.header('EMAIL TESTING', divider='rainbow')
    st.subheader('How to use:')
    st.caption(f'{namespaces}.{{use anything in this section}}@inbox.testmail.app')
    st.subheader('Refresh use "R"')

    emails_by_recipient = {}

    offset = 0
    while True:
        wait_text = st.empty()
        wait_text.text("Please wait...")
        data = get_email_data(tokens, namespaces, offset)
        for email in data["emails"]:
            recipient = email['to']
            if recipient not in emails_by_recipient:
                emails_by_recipient[recipient] = []
            emails_by_recipient[recipient].append(email)
            wait_text.empty()

        if len(data["emails"]) < 100:
            break
        else:
            offset += 100
        wait_text.empty()

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
                
                date_str = datetime.utcfromtimestamp(email['date'] / 1000).replace(tzinfo=timezone.utc).strftime('%d/%m/%Y %H:%M:%S')
                st.write(f"Date: {date_str}")
                st.components.v1.html(email['html'], height=1000, scrolling=True)
                st.header('', divider='green')
