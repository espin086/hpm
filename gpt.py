import openai
import streamlit as st


openai.api_key = st.secrets["openai"]["key"]
openai.organization = st.secrets["openai"]["org"]


def generate_completion(model, role, prompt):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message["content"]
