import os
import streamlit as st
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constant import MODEL

def get_model_client():
    # First try to get API key from session state (web interface)
    api_key = st.session_state.get('api_key')
    
    # If not in session state, try to get from environment variables
    if not api_key:
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError("API key not found. Please set it in the sidebar.")
        
    model_client = OpenAIChatCompletionClient(model=MODEL, api_key=api_key)
    return model_client