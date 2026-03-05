"""
analyze_data.py
---------------
Step 2 of the pipeline: Load the saved headlines CSV and perform
exploratory data analysis (EDA).

What this script does:
  - Loads headlines.csv from the data/ folder
  - Cleans and normalises the text
  - Counts the most frequently used words across all headlines
  - Prints a summary report
  - Saves the word-frequency results to data/word_freq.csv

Usage:
    python src/analyze_data.py
"""

import os
import re
import pandas as pd
from collections import Counter


# ── Configuration ─────────────────────────────────────────────────────────────

INPUT_FILE  = os.path.join("data", "headlines.csv")
OUTPUT_FILE = os.path.join("data", "word_freq.csv")

# Number of top keywords to report
TOP_N = 30

# Words to ignore — these appear everywhere but carry no meaning
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "is", "it", "its", "as", "by", "be", "are", "was", "were",
    "has", "have", "had", "that", "this", "from", "not", "he", "she", "we",
    "they", "you", "i", "his", "her", "their", "our", "will", "can", "may",
    "do", "did", "does", "after", "about", "over", "into", "up", "out",
    "more", "new", "says", "said", "say", "us", "than", "so", "no", "if",
    "what", "how", "who", "which", "when", "than", "been", "also", "could",
    "would", "should", "then", "now", "all", "one", "two", "just", "get",
    "still", "amid", "amid", "amid",
}


# ── Functions ──────────────────────────────────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """Load the headlines CSV and do basic validation."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"File not found: {filepath}\n"
            "  Run fetch_news.py first to generate the data."
        )

    df = pd.read_csv(filepath, parse_dates=["published_at"])
    print(f"Loaded {len(df)} headlines from '{filepath}'.")
    return df


def clean_text(text: str) -> str:
    """
    Lowercase the text and strip everything that is not a letter or space.
    This removes punctuation, numbers, and special characters.
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)  # keep only letters and whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_words(df: pd.DataFrame) -> list[str]:
    """
    Combine all headline titles into one big list of clean words,
    filtering out stopwords and very short words (len < 3).
    """
    all_words = []

    for title in df["title"].dropna():
        cleaned = clean_text(title)
        words = cleaned.split()
        # Keep only meaningful words
        filtered = [w for w in words if w not in STOPWORDS and len(w) >= 3]
        all_words.extend(filtered)

    return all_words


def compute_word_frequency(words: list[str], top_n: int = TOP_N) -> pd.DataFrame:
    """
    Count how often each word appears and return a ranked DataFrame.

    Returns columns: word, count, percentage
    """
    counter = Counter(words)
    most_common = counter.most_common(top_n)

    total = sum(counter.values())

    freq_df = pd.DataFrame(most_common, columns=["word", "count"])
    freq_df["percentage"] = (freq_df["count"] / total * 100).round(2)

    return freq_df


def print_summary(df: pd.DataFrame, freq_df: pd.DataFrame) -> None:
    """Print a human-readable analysis summary to the terminal."""
    print("\n" + "=" * 50)
    print("       NEWS HEADLINE ANALYSIS SUMMARY")
    print("=" * 50)

    print(f"\nTotal headlines analysed : {len(df)}")
    print(f"Date range               : {df['published_at'].min()} → {df['published_at'].max()}")
    print(f"Number of news sources   : {df['source'].nunique()}")

    print(f"\nTop sources by article count:")
    print(df["source"].value_counts().head(5).to_string())

    print(f"\nTop {len(freq_df)} trending keywords:")
    print("-" * 35)
    for _, row in freq_df.iterrows():
        bar = "█" * int(row["percentage"] * 2)  # simple ASCII bar chart
        print(f"  {row['word']:<20} {row['count']:>4}x  {row['percentage']:>5.1f}%  {bar}")

    print("=" * 50)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    df = load_data(INPUT_FILE)

    print("\nExtracting and cleaning words from headlines...")
    words = extract_words(df)
    print(f"  Total meaningful words found: {len(words)}")
    print(f"  Unique words found          : {len(set(words))}")

    freq_df = compute_word_frequency(words, top_n=TOP_N)

    print_summary(df, freq_df)

    # Save word frequencies for the visualiser
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    freq_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nWord frequency data saved → {OUTPUT_FILE}")
    print("Done! Run visualize.py next.")


if __name__ == "__main__":
    main()
