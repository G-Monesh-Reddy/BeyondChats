"""
Streamlit interface for generating and downloading Reddit personas.
"""

import os
import streamlit as st
from app import scrape_reddit_user, generate_persona
from utils import save_persona_as_pdf

st.set_page_config(page_title="Reddit Persona Builder",
                   layout="centered")
st.title("🔎 Reddit User Persona Generator")
st.caption("Powered by Gemini 2.5 Pro + Streamlit")

profile_url = st.text_input(
    "Enter Reddit Profile URL",
    "https://www.reddit.com/user/kojied/"
)

if st.button("Generate Persona"):
    username = profile_url.rstrip("/").split("/")[-1]
    st.info(f"Scraping Reddit user: u/{username}...")

    scraped = scrape_reddit_user(username)
    if not scraped:
        st.error("Unable to scrape Reddit user data.")
    else:
        st.success("Data scraped successfully! 🚀")
        st.info("Generating persona with Gemini…")
        persona = generate_persona("\n".join(scraped))

        st.subheader("🧠 Generated Persona")
        st.text_area("Persona Output", persona, height=400)

        buffer = save_persona_as_pdf(persona, username)
        st.download_button(
            label="📄 Download Persona PDF",
            data=buffer,
            file_name=f"{username}_persona.pdf",
            mime="application/pdf"
        )
