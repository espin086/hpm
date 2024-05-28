import streamlit as st

from gpt import generate_completion

import config


def render_title(role):
    """Render the title and a separator in the Streamlit app."""
    st.title("Chat Response")
    st.write("---")
    st.write(f"Your Role: {role}")  # Display the user-selected role


def render_role_input():
    """Render a text input for the user to set their role."""
    return st.text_input("Enter your role:", "Software Engineer", key="btn_role")


def render_name_input():
    """Render a text input for the user to set their name."""
    return st.text_input("Enter your name:", "", key="btn_name")


def render_slack_messages():
    """Render a text area for the user to input recent Slack messages."""
    return st.text_area("Enter recent Slack messages:", "")


def render_summary_button():
    """Render a button for generating the response."""
    return st.button("Generate Slack Message", key="btn_slack")


def generate_slack_message(model, role, messages):
    """Generate an awesome Slack message based on the input messages."""
    return generate_completion(model, role, messages)


def main():
    user_name = render_name_input()  # Get the user's name
    user_role = render_role_input()  # Get the user's selected role
    slack_messages = render_slack_messages()  # Get the recent Slack messages
    st.write("---")

    prompt = f"""I am {user_name}, a {user_role}, and 
    I want to respond to the following Slack messages. 
    Make the response conversational.  And also make it less than 50 words and well organized, to make it easier to read.
    
    Here are the messages:

    {slack_messages}

    Remember you are {user_name} so respond as {user_name} would.
    
    Response:"""

    if render_summary_button():
        response = generate_slack_message(config.GPT_MODEL, user_role, prompt)
        st.write(response)


if __name__ == "__main__":
    main()
