import streamlit as st
from datetime import datetime
from gpt import generate_completion


ROLE = "You are a Principal Cloud Architect who is writing a weekly report. You need to summarize your accomplishments, challenges, and next steps. The audience are peer and managers who are interested in your work. It is ok to expand on the business benefits of your technical solutions, prefer you do that at the beginning of each bullet point. Use bold and highlighting as needed to stress key words."
MODEL = "gpt-3.5-turbo"

####################################
# UI Components
####################################

# Title
st.title("AISL - Weekly Report")


# Separator
st.write("---")

# Accomplishments Section
st.header("Accomplishments")
accomplishments_input = st.text_area(
    "", help="Enter your accomplishments for the week."
)

# Separator
st.write("---")

# Challenges/Blockers Section
st.header("Challenges/Blockers")
challenges_input = st.text_area(
    "", help="Enter your challenges or blockers for the week."
)

# Separator
st.write("---")

# Next Steps Section
st.header("Next Steps")
next_steps_input = st.text_area("", help="Enter your planned next steps.")


prompt = accomplishments_input + challenges_input + next_steps_input


# Summarize button
if st.button("Summarize", key="btn_summarize"):
    # Accomplishments

    summarize_accomplishments = generate_completion(
        model=MODEL, role=ROLE, prompt=prompt
    )

    st.write("Executive Summmary", summarize_accomplishments)
