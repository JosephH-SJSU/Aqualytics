import os
import openai
import streamlit as st
from PIL import Image
import requests
from openai import OpenAI
from pathlib import Path

st.markdown("# Here is page two")


openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()
