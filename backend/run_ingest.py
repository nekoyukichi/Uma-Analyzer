from __future__ import annotations

import argparse
import json

from app.scrapers.race_scraper import scrape_and_upsert_race


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape a race page and upsert its metadata into Supabase (public.races)."
    )
    parser.add_argument("url", help="Race page URL (netkeiba-like)")
    args = parser.parse_args()

    res = scrape_and_upsert_race(args.url)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
