import streamlit as st

from gpt import generate_completion
import config
from config import UserConfig as UserConfig


def render_title():
    """Render the title and a separator in the Streamlit app."""
    st.title("Chat Response")
    st.write("---")
    st.write(f"Your Role: {UserConfig().job_title}")  # Display the user-selected role


def render_slack_messages():
    """Render a text area for the user to input recent Slack messages."""
    return st.text_area("Slack to respond to:", "")


def render_summary_button():
    """Render a button for generating the response."""
    return st.button("Respond", key="btn_slack")


def generate_slack_message(model, role, messages):
    """Generate an awesome Slack message based on the input messages."""
    return generate_completion(model, role, messages)


def main():
    """Main function for the Slack Response page."""
    slack_messages = render_slack_messages()  # Get the recent Slack messages
    st.write("---")

    name = config.UserConfig().name
    role = config.UserConfig().job_title
    company = config.UserConfig().company

    prompt = f"""I am {name}, a {role}, working at {company} company and 
    I want to respond to the following Slack messages. 
    
    Make the response conversational.  And also make it less than 50 words and well organized, to make it easier to read.
    
    Here are the messages:

    {slack_messages}

    Remember you are a {role} so respond as a {role} would.
    
    Response:"""

    if render_summary_button():
        response = generate_slack_message(config.GPT_MODEL, role, prompt)
        st.write(response)


if __name__ == "__main__":
    main()
