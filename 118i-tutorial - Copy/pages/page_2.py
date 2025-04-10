import openai
from openai import OpenAI
import os
import base64
import requests
import streamlit as st

openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

st.markdown("# Page 2: Water Test Kit Analysis 💧")
st.sidebar.markdown("# Page 2: Water Test Kit Analysis 💧")

water_type = st.selectbox(
    "What type of water are you testing?",
    ["Drinking/Cooking Water", "Bathing/Shower Water", "Face Washing Water", "Laundry Water", "Pet Water", "Plant Water"])
st.info(f" You selected water for: **{water_type}**")

if water_type == "Pet Water":
    pet_type = st.selectbox(
        "What kind of pet is the water for?",
        ["Fish Tank", "Reptile Enclosure", "Dog Bowl", "Cat Fountain"]
    )
    st.info(f"🐾 You selected water for: **{pet_type}**")

if water_type == "Pet Water":
    use_case = f"pet water for a {pet_type.lower()}"
else:
    use_case = water_type.lower()

ref_img = st.file_uploader("📋 Upload Reference Chart", type=["jpg", "jpeg", "png"])
test_img = st.file_uploader("🧪 Upload Test Strip", type=["jpg", "jpeg", "png"])

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

if ref_img and test_img:
    if st.button("🔍 Analyze Water Quality"):
        with st.spinner("Analyzing images with GPT-4 Turbo... 💡"):
            ref_base64 = encode_image(ref_img)
            test_base64 = encode_image(test_img)

            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    f"You are a water quality specialist advising everyday non-expert users. "
                                    f"The user is testing {use_case}. Compare this reference chart to the test strip. "
                                    f"Return water quality readings and how it relates to {use_case} (like pH, copper, nitrate, etc.) in this format:\n\n"
                                    "1. **Summary** – Is the water safe or not?\n"
                                    "2. **Breakdown** – Bullet points for each value with emojis:\n"
                                    "   - ✅ Safe\n"
                                    "   - ⚠️ Caution\n"
                                    "   - 🔴 Problem\n"
                                    "3. **Recommendations** – Simple, clear action steps to improve water quality\n"
                                    "4. **Next Steps** – What to monitor or do next.\n\n"
                                    "Keep language simple, brief, helpful, and friendly. Avoid jargon and lab-only advice."
                                ),
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{ref_base64}"},
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{test_base64}"},
                            },
                        ],
                    }
                ],
                max_tokens=600,
            )

            result = response.choices[0].message.content
            st.subheader("🧠 AI Analysis")
            st.write(result)
else:
    st.info("Please upload both the reference and test strip images to begin.")

st.subheader("💬 Have more questions?")

user_question = st.text_input("Ask a question about a specific value or result (optional):")

if user_question:
    with st.spinner("Getting a detailed answer..."):
        followup_response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a water quality expert giving clear, friendly answers to users testing their water at home.",
                },
                {
                    "role": "user",
                    "content": f"The user was testing {use_case}. They asked: {user_question}",
                }
            ],
            max_tokens=300
        )

        answer = followup_response.choices[0].message.content
        st.markdown("### 📘 Answer")
        st.write(answer)