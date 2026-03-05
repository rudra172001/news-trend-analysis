"""
app.py
------
Flask web application for the News Trend Analysis dashboard.
Runs entirely in-memory — no disk writes — so it deploys cleanly to Vercel.

Local dev:
    python app.py        → visit http://localhost:5000

Vercel deployment:
    Set NEWS_API_KEY in the Vercel dashboard environment variables.
"""

import os
import re
import io
import json
import base64
from collections import Counter
from datetime import datetime, timezone

import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from flask import Flask, render_template, jsonify


# ── App setup ──────────────────────────────────────────────────────────────────

app = Flask(__name__)

API_KEY  = os.getenv("NEWS_API_KEY", "054a11f3fd634d5a90f9c09c25fd2ae6")
BASE_URL = "https://newsapi.org/v2/top-headlines"

STOPWORDS = {
    "the","a","an","and","or","but","in","on","at","to","for","of","with",
    "is","it","its","as","by","be","are","was","were","has","have","had",
    "that","this","from","not","he","she","we","they","you","i","his","her",
    "their","our","will","can","may","do","did","does","after","about","over",
    "into","up","out","more","new","says","said","say","us","than","so","no",
    "if","what","how","who","which","when","been","also","could","would",
    "should","then","now","all","one","two","just","get","still","amid",
}

# Map NewsAPI source names to a short category label for display badges
SOURCE_CATEGORY = {
    "CNN": "Politics", "Fox News": "Politics", "BBC News": "World",
    "Reuters": "World", "AP": "World", "The Guardian": "World",
    "NBC News": "Politics", "ABC News": "Politics", "CBS News": "Politics",
    "MSNBC": "Politics", "Bloomberg": "Business", "Forbes": "Business",
    "The Wall Street Journal": "Business", "Financial Times": "Business",
    "TechCrunch": "Tech", "The Verge": "Tech", "Wired": "Tech",
    "Ars Technica": "Tech", "ESPN": "Sports", "Sky Sports": "Sports",
}


# ── Pipeline helpers ───────────────────────────────────────────────────────────

def fetch_headlines(country: str = "us", category: str = "general") -> list[dict]:
    """Call NewsAPI and return cleaned article dicts."""
    params = {
        "apiKey":   API_KEY,
        "country":  country,
        "category": category,
        "pageSize": 100,
    }
    resp = requests.get(BASE_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "ok":
        raise ValueError(data.get("message", "NewsAPI error"))

    articles = []
    for a in data.get("articles", []):
        title = a.get("title") or ""
        if not title or title == "[Removed]":
            continue
        source = (a.get("source") or {}).get("name", "Unknown")
        articles.append({
            "title":        title,
            "description":  a.get("description") or "",
            "source":       source,
            "category":     SOURCE_CATEGORY.get(source, "News"),
            "published_at": a.get("publishedAt", ""),
            "url":          a.get("url", ""),
            "image":        a.get("urlToImage") or "",
        })
    return articles


def analyse_keywords(articles: list[dict], top_n: int = 30) -> pd.DataFrame:
    """Extract and rank keywords from headline titles."""
    all_words = []
    for a in articles:
        text  = re.sub(r"[^a-z\s]", " ", a["title"].lower())
        words = [w for w in text.split() if w not in STOPWORDS and len(w) >= 3]
        all_words.extend(words)

    counter = Counter(all_words)
    total   = sum(counter.values()) or 1
    rows = [
        {"word": w, "count": c, "percentage": round(c / total * 100, 2)}
        for w, c in counter.most_common(top_n)
    ]
    return pd.DataFrame(rows)


def make_bar_chart_b64(freq_df: pd.DataFrame, top_n: int = 20) -> str:
    """Render bar chart → base64 PNG string (no file write)."""
    top_df = freq_df.head(top_n).iloc[::-1].reset_index(drop=True)
    colors = [
        "#EF5350" if i >= len(top_df) - 5 else "#42A5F5"
        for i in range(len(top_df))
    ]

    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.barh(top_df["word"], top_df["count"], color=colors, edgecolor="none", height=0.65)

    for bar, count in zip(bars, top_df["count"]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                str(count), va="center", ha="left", fontsize=8.5, color="#aaa")

    ax.set_xlabel("Frequency", fontsize=10, color="#888")
    ax.set_title("Top Trending Keywords", fontsize=13, fontweight="bold",
                 pad=10, color="#ddd")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.tick_params(colors="#888")
    for spine in ["top","right","bottom","left"]:
        ax.spines[spine].set_visible(False)

    fig.patch.set_facecolor("#161B22")
    ax.set_facecolor("#161B22")
    ax.tick_params(axis="x", colors="#555")
    ax.tick_params(axis="y", colors="#ccc")

    from matplotlib.patches import Patch
    ax.legend(
        handles=[Patch(facecolor="#EF5350", label="Top 5"),
                 Patch(facecolor="#42A5F5", label="Others")],
        loc="lower right", fontsize=8, facecolor="#21262D",
        edgecolor="#333", labelcolor="#ccc",
    )

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def time_ago(iso_str: str) -> str:
    """Convert ISO timestamp to a human-readable 'X mins ago' string."""
    try:
        dt    = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - dt
        mins  = int(delta.total_seconds() // 60)
        if mins < 1:   return "just now"
        if mins < 60:  return f"{mins}m ago"
        if mins < 1440: return f"{mins // 60}h ago"
        return f"{mins // 1440}d ago"
    except Exception:
        return ""


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    error      = None
    chart_b64  = None
    freq_rows  = []
    headlines  = []
    updated_at = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")

    try:
        articles  = fetch_headlines(country="us", category="general")
        freq_df   = analyse_keywords(articles, top_n=30)
        chart_b64 = make_bar_chart_b64(freq_df, top_n=20)
        freq_rows = freq_df.head(15).to_dict(orient="records")

        # Attach a human-readable time string to each article
        for a in articles:
            a["time_ago"] = time_ago(a["published_at"])
        headlines = articles

    except Exception as exc:
        error = str(exc)

    return render_template(
        "index.html",
        chart_b64  = chart_b64,
        freq_rows  = freq_rows,
        headlines  = headlines,
        updated_at = updated_at,
        error      = error,
    )


@app.route("/api/headlines")
def api_headlines():
    """JSON endpoint — returns latest headlines for the live auto-refresh."""
    try:
        articles = fetch_headlines(country="us", category="general")
        for a in articles:
            a["time_ago"] = time_ago(a["published_at"])
        return jsonify({"status": "ok", "articles": articles,
                        "fetched_at": datetime.now(timezone.utc).isoformat()})
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/trends")
def api_trends():
    """JSON endpoint — returns keyword frequencies."""
    try:
        articles = fetch_headlines(country="us", category="general")
        freq_df  = analyse_keywords(articles, top_n=30)
        return jsonify({"status": "ok",
                        "updated_at": datetime.now(timezone.utc).isoformat(),
                        "trends": freq_df.to_dict(orient="records")})
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
