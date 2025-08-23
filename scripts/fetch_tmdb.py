#!/usr/bin/env python3

"""
Fetch popular films and television series from TMDB with pagination and
save a tidy dataset plus a genre ID→name mapping.

This script expects an .env file in the project root with:
  TMDB_API_KEY=your_key
  LANG=en
  PAGES=15
"""

import os
from pathlib import Path
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.getenv("TMDB_API_KEY")
LANG = os.getenv("LANG", "en")
PAGES = int(os.getenv("PAGES", "10"))  # increase for richer coverage
BASE = "https://api.themoviedb.org/3"

DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def fetch(endpoint: str, params: dict) -> dict:
    """Issue a GET request to TMDB and return JSON (raises for HTTP errors)."""
    r = requests.get(f"{BASE}/{endpoint}", params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def fetch_genre_map() -> dict:
    """Return a combined {genre_id: genre_name} map for film and TV."""
    genres = {}
    for path in ("genre/movie/list", "genre/tv/list"):
        js = fetch(path, {"api_key": API_KEY, "language": LANG})
        for g in js.get("genres", []):
            genres[g["id"]] = g["name"]
    return genres


def collect(kind: str = "movie") -> pd.DataFrame:
    """Collect PAGES of ‘popular’ items for the given kind (movie|tv)."""
    rows = []
    for p in range(1, PAGES + 1):
        js = fetch(
            f"{kind}/popular",
            {"api_key": API_KEY, "language": LANG, "page": p},
        )
        for r in js.get("results", []):
            rows.append(
                {
                    "id": r["id"],
                    "kind": kind,  # 'movie' or 'tv'
                    "title": r.get("title") or r.get("name"),
                    "original_language": r.get("original_language"),
                    "overview": r.get("overview"),
                    "popularity": r.get("popularity"),
                    "vote_average": r.get("vote_average"),
                    "vote_count": r.get("vote_count"),
                    "release_date": r.get("release_date") or r.get("first_air_date"),
                    "genre_ids": r.get("genre_ids", []),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    if not API_KEY:
        raise SystemExit("❌ Please set TMDB_API_KEY in your .env file.")

    df_movies = collect("movie")
    df_tv = collect("tv")
    df = pd.concat([df_movies, df_tv], ignore_index=True)
    df.to_csv(DATA_DIR / "tmdb_popular.csv", index=False)

    gmap = fetch_genre_map()
    pd.Series(gmap).rename("name").to_csv(DATA_DIR / "genres_map.csv", header=True)

    print(
        f"✅ Saved {DATA_DIR/'tmdb_popular.csv'} ({len(df)} rows) "
        f"and {DATA_DIR/'genres_map.csv'} ({len(gmap)} genres)."
    )


if __name__ == "__main__":
    main()