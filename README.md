# 🔍 Reddit Persona Generator

Transform any public Reddit profile into a detailed **user persona** powered by **Gemini AI**. This tool scrapes a user’s posts and comments and generates a professional persona profile which you can **download as a formatted PDF**.

🌐 **Live App:** [redditpersona.streamlit.app](https://redditpersona.streamlit.app)

---

## 📸 Preview

| Input Interface | Output Persona (PDF) |
|-----------------|-----------------------|
| ![Input](assets/input_ui.png) | ![PDF](assets/pdf_sample.png) |

---

## 🚀 Features

- 🔎 Scrapes up to 100 Reddit comments & 50 posts from any username
- 🤖 Uses **Gemini Pro 2.5** LLM to analyze language and build a persona
- 🧠 Persona includes:
  - Age, Occupation, Status, Location
  - Behavioral Archetype
  - Habits, Frustrations, Goals
  - Personality traits (MBTI-style)
- 📄 **One-click PDF export** in clean, visual format

---

## 🧪 Tech Stack

| Layer      | Tech Used                             |
|------------|----------------------------------------|
| Frontend   | Streamlit                              |
| Backend    | PRAW (Reddit API), Gemini AI (Google)  |
| PDF Output | FPDF (template-style layout)           |
| Deployment | Streamlit Cloud                        |

---

## 📦 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/reddit-persona-generator.git
cd reddit-persona-generator
pip install -r requirements.txt
streamlit run ui.py
