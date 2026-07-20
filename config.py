import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# First try Streamlit Secrets, then fall back to .env
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in Streamlit Secrets or .env")