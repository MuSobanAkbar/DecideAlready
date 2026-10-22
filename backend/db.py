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
def saved_tmdb_ids(user_id: str) -> set[int]:
    response = (
        get_client()
        .table(TABLE)
        .select("tmdb_id")
        .eq("user_id", user_id)
        .execute()
    )
    return {row["tmdb_id"] for row in response.data}

def add_to_watch_later(user_id: str, tmdb_id: int, title: str, poster_path: str | None) -> None:
    (
        get_client()
        .table(TABLE)
        .upsert(
            {"user_id": user_id, "tmdb_id": tmdb_id, "title": title, "poster_path": poster_path},
            on_conflict="user_id,tmdb_id",
            ignore_duplicates=True,
        )
        .execute()
    )