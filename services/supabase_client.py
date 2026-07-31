from supabase import Client, create_client

from config import SUPABASE_KEY, SUPABASE_URL


def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

    return create_client(SUPABASE_URL, SUPABASE_KEY)
