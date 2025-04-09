import streamlit as st
import os
import openai
from openai import OpenAI
from pathlib import Path

st.markdown("# Here is page 3")


openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()
