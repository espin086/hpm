import streamlit as st

from chat_response import main as chat_response_main
from daily_standup import main as daily_standup_main
from highlights import main as highlights_main
from write_email import main as email

page = st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to", ["Weekly Updates", "Daily Updates", "Emails", "Slack Response"]
)

if page == "Weekly Updates":
    highlights_main()
if page == "Daily Updates":
    daily_standup_main()
if page == "Emails":
    email()
if page == "Slack Response":
    chat_response_main()
