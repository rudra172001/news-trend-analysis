"""
fetch_news.py
-------------
Step 1 of the pipeline: Fetch real-time top headlines from NewsAPI
and save them as a CSV file in the data/ folder.

Usage:
    python src/fetch_news.py

Requires:
    - A free API key from https://newsapi.org
    - Set your key in the API_KEY variable below (or use an env variable)
"""

import os
import requests
import pandas as pd
from datetime import datetime


# ── Configuration ─────────────────────────────────────────────────────────────

# Replace this with your actual NewsAPI key, or set an environment variable:
#   export NEWS_API_KEY="your_key_here"   (Mac/Linux)
#   set NEWS_API_KEY=your_key_here        (Windows CMD)
API_KEY = os.getenv("NEWS_API_KEY", "054a11f3fd634d5a90f9c09c25fd2ae6")

BASE_URL = "https://newsapi.org/v2/top-headlines"

# How many articles to fetch (max 100 per request on free tier)
PAGE_SIZE = 100

# Output file path
OUTPUT_FILE = os.path.join("data", "headlines.csv")


# ── Functions ──────────────────────────────────────────────────────────────────

def fetch_headlines(country: str = "us", category: str = "general") -> list[dict]:
    """
    Call the NewsAPI and return a list of article dictionaries.

    Args:
        country:  Two-letter country code (e.g. "us", "gb", "in").
        category: News category — general, business, technology, science,
                  health, sports, entertainment.

    Returns:
        A list of raw article dicts from the API response.
    """
    params = {
        "apiKey":   API_KEY,
        "country":  country,
        "category": category,
        "pageSize": PAGE_SIZE,
    }

    print(f"Fetching top-{PAGE_SIZE} '{category}' headlines for country='{country}'...")
    response = requests.get(BASE_URL, params=params, timeout=10)

    # Raise an exception for HTTP errors (4xx / 5xx)
    response.raise_for_status()

    data = response.json()

    if data.get("status") != "ok":
        raise ValueError(f"NewsAPI error: {data.get('message', 'Unknown error')}")

    articles = data.get("articles", [])
    print(f"  Retrieved {len(articles)} articles.")
    return articles


def parse_articles(articles: list[dict]) -> pd.DataFrame:
    """
    Extract the relevant fields from raw API articles and return a DataFrame.

    We keep: title, description, source name, published date, and the URL.
    """
    rows = []
    for article in articles:
        rows.append({
            "title":       article.get("title", ""),
            "description": article.get("description", ""),
            "source":      article.get("source", {}).get("name", ""),
            "published_at": article.get("publishedAt", ""),
            "url":         article.get("url", ""),
        })

    df = pd.DataFrame(rows)

    # Convert published_at to a proper datetime column
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")

    # Drop rows where the title is missing — they are useless for analysis
    df.dropna(subset=["title"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def save_to_csv(df: pd.DataFrame, filepath: str) -> None:
    """Save the DataFrame to a CSV file, creating parent directories if needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False, encoding="utf-8")
    print(f"  Saved {len(df)} rows → {filepath}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if API_KEY == "YOUR_API_KEY_HERE":
        print(
            "\n[ERROR] No API key found.\n"
            "  1. Get a free key at https://newsapi.org\n"
            "  2. Set it in this file or as the NEWS_API_KEY environment variable.\n"
        )
        return

    articles = fetch_headlines(country="us", category="general")
    df = parse_articles(articles)

    print(f"\nSample data preview:")
    print(df[["title", "source", "published_at"]].head(5).to_string(index=False))

    save_to_csv(df, OUTPUT_FILE)
    print("\nDone! Run analyze_data.py next.")


if __name__ == "__main__":
    main()
