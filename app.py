import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))  # Ensure the app finds the module
from email_sender import send_bulk_emails


st.title("Cold Email Automation Tool")

SHEET_URL = st.text_input("https://docs.google.com/spreadsheets/d/1NE4yDH-WG2k80ov5gWgKOwuGffx8Hh_4nOQVkwDKlFQ/edit?usp=sharing")
SHEET_NAME = st.text_input("Main")

if st.button("Send Emails"):
    if SHEET_URL and SHEET_NAME:
        send_bulk_emails(SHEET_URL, SHEET_NAME)
        st.success("Emails sent successfully!")
    else:
        st.error("Please provide the Google Sheets URL and Sheet Name.")