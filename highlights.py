"""This module is a Streamlit app for generating a weekly report for AISL.
"""

import streamlit as st

from gpt import generate_completion

import config

HOW_TO_SUMMARIZE = """You need to summarize your accomplishments, challenges, and next steps.
The audience are peer and managers who are interested in your work.
It is ok to expand on the business benefits of your accomplishments,
prefer you do that at the beginning of each bullet point.
Any challenges or blockers should be addressed and next steps should be recommended.
Use bold and highlighting as needed to stress key words. You must have 3 sections in your response:

Accomplishments:

Challenges/Blockers:

Next Steps

"""


def render_title(role):
    """Render the title and a separator in the Streamlit app."""
    st.title("Weekly Hightlights")
    st.write(f"Role: {role}")  # Display the user-selected role


def render_role_input():
    """Render a text input for the user to set their role."""
    return st.text_input("Enter your role:", "Principal Cloud Architect")


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
    return st.button("Summarize", key="btn_summarize")


def get_summary(model, role, prompt):
    """Get a summary text generated by GPT.

    Parameters:
        model (str): The GPT model to use.
        role (str): The role description for the prompt.
        prompt (str): The prompt text to summarize.

    Returns:
        str: The generated summary text.
    """
    return generate_completion(model, role, prompt)


def main():
    """Main function to render the Streamlit app."""

    st.header("Accomplishments")
    accomplishments_input = render_text_area(
        "Accomplishments", "Enter your accomplishments for the week."
    )
    st.write("---")

    st.header("Challenges/Blockers")
    challenges_input = render_text_area(
        "Challenges/Blockers", "Enter your challenges or blockers for the week."
    )
    st.write("---")

    st.header("Next Steps")
    next_steps_input = render_text_area("Next Steps", "Enter your planned next steps.")

    prompt = (
        HOW_TO_SUMMARIZE + accomplishments_input + challenges_input + next_steps_input
    )

    if render_summary_button():
        summary = get_summary(config.GPT_MODEL, config.UserConfig().job_title, prompt)
        st.write(summary)


if __name__ == "__main__":
    main()
