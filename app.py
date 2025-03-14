import streamlit as st
from email_sender import send_bulk_emails  
import streamlit as st
import subprocess

installed_packages = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
st.text(installed_packages.stdout)

st.title("Cold Email Automation Tool")

SHEET_URL = st.text_input("Enter Google Sheets URL", "https://docs.google.com/spreadsheets/d/1NE4yDH-WG2k80ov5gWgKOwuGffx8Hh_4nOQVkwDKlFQ/edit")
SHEET_NAME = st.text_input("Enter Sheet Name", "Main")

if st.button("Send Emails"):
    if SHEET_URL and SHEET_NAME:
        send_bulk_emails(SHEET_URL, SHEET_NAME)
        st.success("Emails sent successfully!")
    else:
        st.error("Please provide the Google Sheets URL and Sheet Name.")