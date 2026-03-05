"""
visualize.py
------------
Step 3 of the pipeline: Load the word-frequency data and produce
two visualisations:
  1. Horizontal bar chart  — top trending keywords
  2. Word cloud            — visual summary of all keywords

Output images are saved to data/ so you can include them in reports.

Usage:
    python src/visualize.py

Optional dependency (word cloud):
    pip install wordcloud
    If wordcloud is not installed the bar chart still works fine.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# wordcloud is optional — we handle the import gracefully
try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False


# ── Configuration ─────────────────────────────────────────────────────────────

INPUT_FILE      = os.path.join("data", "word_freq.csv")
BAR_CHART_FILE  = os.path.join("data", "trending_keywords.png")
WORDCLOUD_FILE  = os.path.join("data", "wordcloud.png")

# How many keywords to show in the bar chart
TOP_N = 20

# Colour palette for the bars
BAR_COLOR = "#2196F3"       # material blue
HIGHLIGHT_COLOR = "#F44336" # red — top 5 words stand out


# ── Functions ──────────────────────────────────────────────────────────────────

def load_word_freq(filepath: str) -> pd.DataFrame:
    """Load the word frequency CSV produced by analyze_data.py."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"File not found: {filepath}\n"
            "  Run analyze_data.py first."
        )
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} keywords from '{filepath}'.")
    return df


def plot_bar_chart(df: pd.DataFrame, top_n: int = TOP_N) -> None:
    """
    Draw a horizontal bar chart of the top-N trending keywords.

    The top 5 bars are highlighted in red to draw the eye to the
    most dominant topics.
    """
    top_df = df.head(top_n).copy()

    # Reverse so the highest bar is at the top of the chart
    top_df = top_df.iloc[::-1].reset_index(drop=True)

    # Colour the top 5 differently
    colors = [
        HIGHLIGHT_COLOR if i >= (len(top_df) - 5) else BAR_COLOR
        for i in range(len(top_df))
    ]

    fig, ax = plt.subplots(figsize=(10, 8))

    bars = ax.barh(top_df["word"], top_df["count"], color=colors, edgecolor="white")

    # Add count labels at the end of each bar
    for bar, count in zip(bars, top_df["count"]):
        ax.text(
            bar.get_width() + 0.3,
            bar.get_y() + bar.get_height() / 2,
            str(count),
            va="center",
            ha="left",
            fontsize=9,
            color="#333333",
        )

    ax.set_xlabel("Frequency (number of headlines)", fontsize=11)
    ax.set_title("Top Trending Keywords in Today's News Headlines", fontsize=14, fontweight="bold", pad=15)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=HIGHLIGHT_COLOR, label="Top 5 keywords"),
        Patch(facecolor=BAR_COLOR,       label="Other keywords"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=9)

    plt.tight_layout()
    plt.savefig(BAR_CHART_FILE, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Bar chart saved → {BAR_CHART_FILE}")


def plot_wordcloud(df: pd.DataFrame) -> None:
    """
    Generate a word cloud image where larger words = higher frequency.

    Requires the 'wordcloud' package: pip install wordcloud
    """
    if not WORDCLOUD_AVAILABLE:
        print("  [Skipping word cloud] Install it with: pip install wordcloud")
        return

    # Build a dict of {word: frequency} for the WordCloud generator
    word_freq = dict(zip(df["word"], df["count"]))

    wc = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        colormap="Blues",
        max_words=100,
        prefer_horizontal=0.85,
    ).generate_from_frequencies(word_freq)

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("News Keyword Word Cloud", fontsize=16, fontweight="bold", pad=12)

    plt.tight_layout()
    plt.savefig(WORDCLOUD_FILE, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Word cloud saved → {WORDCLOUD_FILE}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    df = load_word_freq(INPUT_FILE)

    print("\nGenerating visualisations...")
    plot_bar_chart(df, top_n=TOP_N)
    plot_wordcloud(df)

    print("\nDone! Check the data/ folder for your charts.")
    print(f"  {BAR_CHART_FILE}")
    if WORDCLOUD_AVAILABLE:
        print(f"  {WORDCLOUD_FILE}")


if __name__ == "__main__":
    main()
