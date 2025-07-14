import streamlit as st
from app import scrape_reddit_user, generate_persona
from utils import save_persona_as_pdf

st.set_page_config(page_title="Reddit Persona Generator", layout="centered")
st.title("🔎 Reddit User Persona Generator")
st.caption("Powered by Gemini 2.5 Pro + Streamlit")

profile_url = st.text_input("Enter Reddit Profile URL:", "https://www.reddit.com/user/kojied/")

if st.button("Generate Persona"):
    username = profile_url.strip('/').split('/')[-1]
    st.info(f"Scraping Reddit user: {username}...")
    scraped_data = scrape_reddit_user(username)

    if scraped_data:
        st.success("✅ Data scraped successfully!")
        st.info("🎯 Generating persona with Gemini...")
        user_data = "\n".join(scraped_data)
        persona = generate_persona(user_data)

        st.subheader("🧠 Persona")
        st.text_area("Generated Persona", persona, height=400)

        # PDF download
        pdf_buffer = save_persona_as_pdf(persona, username)
        st.download_button(
            label="📄 Download Persona PDF",
            data=pdf_buffer,
            file_name=f"{username}_persona.pdf",
            mime="application/pdf"
        )
    else:
        st.error("❌ Could not scrape Reddit user data.")
