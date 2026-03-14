from supabase import create_client
from dotenv import load_dotenv
import streamlit as st
import os

# Load environment variables (works locally with .env file)
load_dotenv()


def get_secret(key):
    """
    Get a secret from os.getenv first (local .env), then st.secrets (Streamlit Cloud).
    """
    value = os.getenv(key)
    if value:
        return value
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return None


def get_supabase():
    """
    Returns a Supabase client using credentials from .env or st.secrets
    """
    url = get_secret("SUPABASE_URL")
    key = get_secret("SUPABASE_KEY")

    if not url or not key:
        raise Exception("Supabase credentials missing. Add them to .env (local) or Streamlit Secrets (cloud).")

    supabase = create_client(url, key)
    return supabase