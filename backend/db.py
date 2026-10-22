"""Adapter for our database (Supabase Postgres).

Routes call these functions. Nothing outside this file imports `supabase`.
Every function takes a user_id and only touches that user's rows.
"""
import os
from functools import lru_cache

from supabase import Client, create_client

TABLE = "watch_later"


@lru_cache(maxsize=1)
def get_client() -> Client:
    return create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SECRET_KEY"],
    )