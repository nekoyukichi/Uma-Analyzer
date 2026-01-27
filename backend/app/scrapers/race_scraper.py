from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd
import requests
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class RaceResultRow:
    finish_position: int
    horse_name: str


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


def rows_to_dataframe(rows: Iterable[RaceResultRow]) -> pd.DataFrame:
    return pd.DataFrame(
        [{"finish_position": r.finish_position, "horse_name": r.horse_name} for r in rows]
    )


