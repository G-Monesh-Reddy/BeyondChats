import google.generativeai as genai

# Print version to confirm
print("google-generativeai version:", genai.__version__)

# Configure your API key
genai.configure(api_key="AIzaSyB8PdMhqufy9g41jOA_-j1d9DkgQNC4KL4")  # Replace with your actual key

# List all available models


# Use the correct model name from the list
try:
    model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")  # ✅ Updated model name
    response = model.generate_content("Give abt sample introduction of gemini ai")
    print("\n🤖 Gemini says:", response.text)
except Exception as e:
    print("\n❌ Error:", e)
