from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re
from typing import Iterable

import pandas as pd
import requests
from bs4 import BeautifulSoup

from app.services.db_service import RaceRecord, get_supabase_client, upsert_race


@dataclass(frozen=True)
class RaceResultRow:
    finish_position: int
    horse_name: str


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def _extract_first_non_empty_text(soup: BeautifulSoup, selectors: list[str]) -> str | None:
    for selector in selectors:
        el = soup.select_one(selector)
        if el is None:
            continue
        text = _normalize_text(el.get_text(" ", strip=True))
        if text:
            return text
    return None


def _extract_race_name(soup: BeautifulSoup, race_id: str) -> str:
    raw_name = _extract_first_non_empty_text(
        soup,
        ["h1", ".RaceName", "meta[property='og:title']", "title"],
    )
    if not raw_name:
        return f"race:{race_id}"

    # Drop common suffixes in title text.
    name = raw_name.split("|", 1)[0].strip()
    name = name.split("｜", 1)[0].strip()
    return name or f"race:{race_id}"


def _extract_course(data_text: str) -> str:
    courses = ["札幌", "函館", "福島", "新潟", "東京", "中山", "中京", "京都", "阪神", "小倉"]
    pattern = r"\d+回\s*(" + "|".join(courses) + r")\s*\d+日目"
    m = re.search(pattern, data_text)
    if m:
        return m.group(1)

    for c in courses:
        if c in data_text:
            return c
    return "UNKNOWN"


def _extract_race_id_from_url(url: str) -> str:
    # netkeiba-like patterns: .../race/202305030811/ or ?race_id=...
    m = re.search(r"race_id=(\d+)", url)
    if m:
        return m.group(1)
    m = re.search(r"/race/(\d+)/", url)
    if m:
        return m.group(1)
    m = re.search(r"(\d{10,})", url)
    if m:
        return m.group(1)
    return url


def parse_race_metadata(html: str, *, url: str) -> RaceRecord:
    """
    Best-effort extraction of race metadata to fit the `public.races` schema.
    When fields cannot be extracted, safe defaults are applied.
    """
    soup = BeautifulSoup(html, "html.parser")

    race_id = _extract_race_id_from_url(url)

    race_name = _extract_race_name(soup, race_id)

    # netkeiba-like race data text blob
    data_text = ""
    data_el = soup.select_one(".RaceData01") or soup.select_one(".RaceData02") or soup.select_one("body")
    if data_el:
        data_text = _normalize_text(data_el.get_text(" ", strip=True))

    # held_on (YYYY年MM月DD日)
    held_on = date.today()
    m = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", data_text)
    if m:
        held_on = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    # track_type + distance_m (芝2000m / ダ1800m etc.)
    track_type = "UNKNOWN"
    distance_m = 1200
    m = re.search(r"(芝|ダート|ダ)[^0-9]{0,10}?(\d{3,4})m", data_text)
    if m:
        track_type = "ダート" if m.group(1) in ("ダ", "ダート") else "芝"
        distance_m = int(m.group(2))

    # course (開催場)
    # Prefer explicit patterns like "3回東京8日目" to avoid false positives from side links.
    course = _extract_course(data_text)

    weather = None
    m = re.search(r"天候\s*[:：]\s*([^\s/]+)", data_text)
    if m:
        weather = m.group(1).strip()

    track_condition = None
    m = re.search(r"(?:芝|ダート|ダ)\s*[:：]\s*([^\s/]+)", data_text)
    if m:
        track_condition = m.group(1).strip()

    return RaceRecord(
        race_id=race_id,
        held_on=held_on,
        race_name=race_name,
        course=course,
        track_type=track_type,
        distance_m=distance_m,
        weather=weather,
        track_condition=track_condition,
        raw_source_url=url,
    )


def fetch_html(url: str, *, timeout_seconds: int = 20) -> str:
    """
    Fetch HTML from a race page URL.

    Notes:
    - This is a baseline implementation. Netkeiba (etc.) may block scraping depending on headers/rate-limits.
    - Keep it simple for now: add a User-Agent and use a timeout.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=timeout_seconds)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    return resp.text


def parse_race_results(html: str) -> list[RaceResultRow]:
    """
    Parse race results from HTML and return (finish_position, horse_name) rows.

    Assumed HTML structure (netkeiba-like):
    - A results table exists (e.g., class="race_table_01")
    - Each row has a finish position cell (e.g., class="rank")
    - Each row has a horse name link (e.g., class="horse_name" <a>Horse</a>)
    """
    soup = BeautifulSoup(html, "html.parser")

    table = soup.select_one("table.race_table_01") or soup.select_one("table")
    if table is None:
        return []

    results: list[RaceResultRow] = []
    for tr in table.select("tr"):
        rank_el = tr.select_one("td.rank") or tr.select_one("td:nth-child(1)")
        horse_el = tr.select_one("td.horse_name a") or tr.select_one(
            "td.horse a"
        )
        if rank_el is None or horse_el is None:
            continue

        rank_text = rank_el.get_text(strip=True)
        horse_name = horse_el.get_text(strip=True)

        # Skip header-like rows or empty rows.
        if not rank_text or not horse_name:
            continue

        # "取消/除外/中止" etc. are possible; keep only integer ranks.
        try:
            finish_position = int(rank_text)
        except ValueError:
            continue

        results.append(RaceResultRow(finish_position=finish_position, horse_name=horse_name))

    return results


def scrape_race_horses_and_positions(url: str) -> pd.DataFrame:
    """
    High-level helper:
    - fetch race HTML
    - parse rows
    - return as pandas.DataFrame
    """
    html = fetch_html(url)
    rows = parse_race_results(html)
    return pd.DataFrame(
        [{"finish_position": r.finish_position, "horse_name": r.horse_name} for r in rows]
    )


def scrape_and_upsert_race(url: str) -> dict:
    """
    Convenience helper:
    - fetch HTML
    - parse metadata for `public.races`
    - upsert to Supabase
    """
    html = fetch_html(url)
    race = parse_race_metadata(html, url=url)
    client = get_supabase_client()
    return upsert_race(client, race)


def rows_to_dataframe(rows: Iterable[RaceResultRow]) -> pd.DataFrame:
    return pd.DataFrame(
        [{"finish_position": r.finish_position, "horse_name": r.horse_name} for r in rows]
    )
