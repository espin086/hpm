import streamlit as st

from gpt import generate_completion

MODEL = "gpt-3.5-turbo"


def render_title(role):
    """Render the title and a separator in the Streamlit app."""
    st.title("Email Writer")
    st.write("---")
    st.write(f"Your Role: {role}")  # Display the user-selected role


def render_role_input():
    """Render a text input for the user to set their role."""
    return st.text_input("Enter your role:", "Software Engineer")


def render_text_area(section_title, help_text):
    """Render a text area component in the Streamlit app.

    Parameters:
        section_title (str): The title for this section.
        help_text (str): The help text for the text area.

    Returns:
        str: The text entered by the user in the text area.
    """
    return st.text_area("", help=help_text, key=section_title)


def render_summary_button():
    """Render a button for summarizing the input.

    Returns:
        bool: True if the button is clicked, False otherwise.
    """
    return st.button("Write Email", key="btn_email")


def write_email(model, role, prompts):
    return generate_completion(model, role, prompts)


def main():
    user_role = render_role_input()  # Get the user's selected role
    render_title(user_role)  # Pass the user's role to the title function

    st.header("Recipient Name")
    email_to = render_text_area("To", "Enter the recipient's name.")
    st.header("How are they? (Boss, colleague, etc.)")
    email_to_role = render_text_area("How are they?", "Boss, colleague, etc.")
    st.header("What's Your Name")
    email_from = render_text_area("From", "Enter your name.")
    st.header("What do you want to say? (Notes)")
    email_input = render_text_area("What do you want to say?", "Enter your notes")
    st.write("---")

    prompt = f"""
    Write a professional email to {email_to} ({email_to_role}) from {email_from} about {email_input}.
    
    You will want to structure your response like this:

    Name of recipient: (here you will write the name of the recipient, don't write Dear, that's awkward)

    Subject: (here you will write the subject of your email)

    here you will write the body of your email, you will use bold and bullet points to hit the key points of your email.

    Note: Please don't write Dear{email_to}, that's awkward. Instead, just write {email_to}.
    
    Style Guide: Used bold and bullet points to hit the key points of your email.

    """

    if render_summary_button():
        summary = write_email(MODEL, user_role, prompt)
        st.write(summary)


if __name__ == "__main__":
    main()
