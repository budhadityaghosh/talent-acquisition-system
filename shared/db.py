from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_supabase():
    """
    Returns a Supabase client using credentials from .env
    """

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise Exception("Supabase credentials missing in .env")

    supabase = create_client(url, key)

    return supabase