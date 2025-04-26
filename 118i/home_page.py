import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image

# Coded with the aid of ChatGPT to format title and logo.
col1, col2 = st.columns([1, 5])  # Adjust ratio for spacing

with col1:
    logo = Image.open("images/Aqualytics_Logo_Cleaned.png")
    st.image(logo, width= 150)

with col2:
    st.markdown("<h1 style='margin-bottom: 0;'>Aqualytics</h1>", unsafe_allow_html=True)
    st.markdown("##### Smart Water Quality Analysis, Powered by AI")

st.markdown("### Welcome to Aqualytics!")

st.markdown("""
Designed to make water quality information clear, actionable, and accessible for everyone.
""")

st.markdown("- **Page 1**: Ask questions about complex water quality reports, such as those from Silicon Valley Water. Our AI breaks down confusing jargon and numbers into simple, helpful insights.")
st.image("images/valley_water.png", caption="Sillicon Valley Water Quality Report", use_container_width=True)

st.markdown("- **Page 2**: Upload your own home water test kit results. Aqualytics will analyze them for you using AI, helping you understand exactly what the colors mean and whether your water is safe.")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(
        "images/test_kit_results.png",
        caption="Test Kit Result Example (AI Generated)",
        width=300
    )

st.markdown("- **Page 3**: If your water appears unsafe, report it directly through the app. Your report helps raise awareness in your district and encourages proactive community responses.")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(
        "images/report_example.png",
        caption="Reporting Issue Example (AI Generated)",
        width=300
    )

st.markdown("""
Together, we can make water safety smarter, faster, and more transparent. 💧
""")
