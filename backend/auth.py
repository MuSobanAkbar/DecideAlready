import os
from functools import lru_cache

import jwt
from fastapi import Header, HTTPException


@lru_cache(maxsize=1)
def get_jwks_client() -> jwt.PyJWKClient:
    supabase_url = os.environ["SUPABASE_URL"]
    return jwt.PyJWKClient(f"{supabase_url}/auth/v1/.well-known/jwks.json")


def get_current_user_id(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Please sign in.")

    token = authorization.removeprefix("Bearer ")
    supabase_url = os.environ["SUPABASE_URL"]

    try:
        signing_key = get_jwks_client().get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256"],
            audience="authenticated",
            issuer=f"{supabase_url}/auth/v1",
        )
    except jwt.PyJWTError:
        raise HTTPException(401, "Your sign-in has expired. Please sign in again.")

    return claims["sub"]