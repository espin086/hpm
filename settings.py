import streamlit as st
from config import UserConfig


def main():
    """Main function for the settings page"""
    st.title("Settings")

    # Create an instance of UserConfig
    config = UserConfig()

    # Create text input fields for each attribute
    name = st.text_input("Name", config.name)
    job_title = st.text_input("Job Title", config.job_title)
    company = st.text_input("Company", config.company)

    # Update button
    if st.button("Update"):
        config.name = name
        config.job_title = job_title
        config.company = company
        st.success("Settings updated successfully!")

    # Display current settings
    st.subheader("Current Settings")
    st.text(f"Name: {config.name}")
    st.text(f"Job Title: {config.job_title}")
    st.text(f"Company: {config.company}")


if __name__ == "__main__":
    main()
