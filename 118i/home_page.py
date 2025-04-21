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
    st.sidebar.markdown("# Main Page")

st.markdown("""
### 💧 Welcome to Aqualytics!
**Your AI-powered assistant for understanding and improving water quality.**

Aqualytics is designed to make water quality information clear, actionable, and accessible for everyone — no science degree required.

- **Page 1**: Ask questions about complex water quality reports, such as those from Silicon Valley Water. Our AI breaks down confusing jargon and numbers into simple, helpful insights.  
- **Page 2**: Upload your own home water test kit results. Aqualytics will analyze them for you using AI, helping you understand exactly what the colors mean and whether your water is safe.  
- **Page 3**: If your water appears unsafe, report it directly through the app. Your report helps raise awareness in your district and encourages proactive community responses.

Together, we can make water safety smarter, faster, and more transparent. 💧
""")
