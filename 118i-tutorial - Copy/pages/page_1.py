import os
import openai
import streamlit as st
from openai import OpenAI


st.markdown("# Here is Page 1")

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()
