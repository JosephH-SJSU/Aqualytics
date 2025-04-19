import openai
from openai import OpenAI
import os
import base64
import requests
import streamlit as st

from openai import OpenAI
client = OpenAI()

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "replace\\with\\image\\path.png"

# Getting the Base64 string
base64_image = encode_image(image_path)
with st.form(key = "chat"):
    st.markdown("# Ask about the most recent water quality report")
    prompt = st.text_input("Please ask a question about the Water Quality report: ") 
    
    submitted = st.form_submit_button("Submit")
    

    if submitted:
        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "user",
                    "content": [
                        { "type": "text", "text": prompt },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
        )

        print(completion.choices[0].message.content)

        st.write(completion.choices[0].message.content)
# create our streamlit app
