import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constant import MODEL

def get_model_client():
    # Try to get API key from environment variables first
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    # If not in environment, try to get from Streamlit session state (only if running in Streamlit)
    if not api_key:
        try:
            import streamlit as st
            api_key = st.session_state.get('api_key')
        except:
            pass
    
    if not api_key:
        raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable or use the web interface.")
        
    model_client = OpenAIChatCompletionClient(model=MODEL, api_key=api_key)
    return model_client