import openai
from openai import OpenAI
import os
import base64
import requests
import streamlit as st

openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "images/WaterQuality_Photo.png"

# Getting the Base64 string
base64_image = encode_image(image_path)
with st.form(key = "chat"):
    st.markdown("# Water Quality Report Assistant")
    st.image("images/WaterQuality_Photo.png", "Water Quality Report Table")
    st.markdown("[Click here to check validity](https://s3.us-west-1.amazonaws.com/valleywater.org.us-west-1/s3fs-public/2025-04/2025_03%20March%20Water%20Quality%20Report.pdf)")
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
