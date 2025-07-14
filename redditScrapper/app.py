import os
from datetime import datetime
from dotenv import load_dotenv
import praw
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")  # ✅ Fixed model name

# Scrape Reddit user data
def scrape_reddit_user(username):
    try:
        user = reddit.redditor(username)
        comments = [
            f"[Comment] {comment.body.strip()} (Score: {comment.score})"
            for comment in user.comments.new(limit=100)
        ]
        posts = [
            f"[Post] {post.title.strip()} - {post.selftext.strip()[:500]} (Score: {post.score})"
            for post in user.submissions.new(limit=50)
        ]
        return posts + comments
    except Exception as e:
        print(f"❌ Error scraping Reddit user: {e}")
        return []

# Generate persona using Gemini
def generate_persona(user_data_text):
    if not user_data_text.strip():
        return "No Reddit data available to generate persona."

    prompt = f"""
Analyze the following Reddit user data and generate a detailed user persona with the structure below:

Include:
- Age, Occupation, Status, Location (if available)
- Archetype
- Behaviour & Habits
- Frustrations
- Motivations
- Goals & Needs
- Personality (on MBTI scale)

For each insight, cite the source with a quote or post.

Reddit User Data:
{user_data_text}
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini error: {e}"

# Save output
def save_persona_to_file(persona_text, username):
    filename = f"{username}_persona_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(persona_text)
        print(f"✅ Persona saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

# Main logic
def build_user_persona(profile_url):
    username = profile_url.strip('/').split('/')[-1]
    print(f"\n🔍 Scraping Reddit user: {username}")
    scraped_data = scrape_reddit_user(username)
    if not scraped_data:
        print("⚠️ No data found.")
        return

    user_data_text = '\n'.join(scraped_data)
    print("🤖 Generating persona using Gemini AI...")
    persona = generate_persona(user_data_text).strip()
    print("\n📝 Preview:\n" + persona[:500] + "\n...")

    save_persona_to_file(persona, username)

# Entry point
if __name__ == "__main__":
    reddit_profile = "https://www.reddit.com/user/kojied/"
    build_user_persona(reddit_profile)
