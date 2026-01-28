from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from datetime import date
from typing import Any, Optional

from dotenv import find_dotenv, load_dotenv
from supabase import Client, create_client


@dataclass(frozen=True)
class RaceRecord:
    race_id: str
    held_on: date
    race_name: str
    course: str
    track_type: str
    distance_m: int
    race_class: Optional[str] = None
    weather: Optional[str] = None
    track_condition: Optional[str] = None
    raw_source_url: Optional[str] = None


def _get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise RuntimeError(
            f"Missing environment variable: {name}. "
            f"Set it in .env (see .env.example)."
        )
    return value


def get_supabase_client() -> Client:
    """Create a Supabase client using SUPABASE_URL / SUPABASE_ANON_KEY."""
    # Try to load the nearest .env (repo root or backend/.env) when running scripts.
    env_path = find_dotenv(usecwd=True)
    if env_path:
        load_dotenv(env_path)

    url = _get_env("SUPABASE_URL")
    key = _get_env("SUPABASE_ANON_KEY")
    return create_client(url, key)


def upsert_race(client: Client, race: RaceRecord) -> dict[str, Any]:
    """Upsert into public.races using race_id as the primary key."""
    payload = asdict(race)
    # Supabase expects ISO strings for dates.
    payload["held_on"] = race.held_on.isoformat()

    # on_conflict ensures we do not create duplicates for the same race_id.
    res = (
        client.table("races")
        .upsert(payload, on_conflict="race_id")
        .execute()
    )

    # supabase-py returns PostgrestResponse-like object with .data
    data = getattr(res, "data", None)
    if data is None:
        return {"data": None}
    return {"data": data}
