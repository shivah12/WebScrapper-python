import openai
import streamlit as st

client = openai.OpenAI(api_key=st.secrets["openai"]["OPENAI_API_KEY"])

def interpret_prompt(prompt, url):
    try:
        system_message = (
            "You're a web scraping assistant. Convert the user prompt into a CSS selector "
            "or scraping rule that can be used to extract data from the given webpage."
        )

        user_message = f"URL: {url}\nInstruction: {prompt}"

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.2,
        )

        selector = response.choices[0].message.content.strip()
        return selector
    except Exception as e:
        print(f"Error in AI interpretation: {e}")
        return "body"  # fallback selector
