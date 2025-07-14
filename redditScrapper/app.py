"""
Core logic: scrape Reddit user data, generate persona via Gemini.
"""

import os
from dotenv import load_dotenv
import praw
import google.generativeai as genai

# Load environment variables
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")


def scrape_reddit_user(username: str) -> list[str]:
    """
    Scrape the user's latest Reddit comments and posts.
    Returns a list of text strings.
    """
    try:
        user = reddit.redditor(username)
        comments = [
            f"[Comment] {c.body} (Score: {c.score})"
            for c in user.comments.new(limit=100)
        ]
        posts = [
            f"[Post] {p.title} - {p.selftext[:300]} (Score: {p.score})"
            for p in user.submissions.new(limit=50)
        ]
        return posts + comments
    except Exception as exc:
        print(f"Error scraping user {username!r}: {exc}")
        return []


def generate_persona(user_data_text: str) -> str:
    """
    Use Gemini to generate a detailed persona based on Reddit data.
    """
    if not user_data_text.strip():
        return "No Reddit data available to generate persona."

    prompt = (
        "Analyze the following Reddit user data and generate a detailed "
        "user persona with sections: Basic Info, Archetype, Behaviour & "
        "Habits, Frustrations, Motivations, Goals & Needs, Personality.\n\n"
        f"Reddit Data:\n{user_data_text}"
    )

    try:
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as exc:
        return f"⚠️ Gemini error: {exc}"
