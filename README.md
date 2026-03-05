# News Trend Analysis

A beginner-friendly Python data analytics project that fetches real-time news headlines, identifies the most trending keywords, and visualises the results.

---

## What This Project Does

1. **Fetches** top news headlines from [NewsAPI](https://newsapi.org)
2. **Stores** them as a CSV dataset in the `data/` folder
3. **Analyses** the headlines to find the most frequent keywords
4. **Visualises** the trends as a bar chart and optional word cloud

---

## Project Structure

```
news-trend-analysis/
│
├── data/                    # Auto-generated output files
│   ├── headlines.csv        # Raw fetched headlines
│   ├── word_freq.csv        # Keyword frequency table
│   ├── trending_keywords.png
│   └── wordcloud.png
│
├── src/
│   ├── fetch_news.py        # Step 1 — fetch & save headlines
│   ├── analyze_data.py      # Step 2 — clean text & count keywords
│   └── visualize.py         # Step 3 — generate charts
│
├── notebook.ipynb           # Interactive Jupyter notebook (full pipeline)
├── requirements.txt
└── README.md
```

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/news-trend-analysis.git
cd news-trend-analysis
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

To also enable the word cloud:

```bash
pip install wordcloud
```

To run the Jupyter notebook:

```bash
pip install jupyter
```

### 3. Get a free NewsAPI key

1. Go to [https://newsapi.org](https://newsapi.org) and sign up for a free account.
2. Copy your API key from the dashboard.
3. Set it as an environment variable **or** paste it directly in `fetch_news.py`.

**Environment variable (recommended):**

```bash
# Mac / Linux
export NEWS_API_KEY="your_key_here"

# Windows CMD
set NEWS_API_KEY=your_key_here

# Windows PowerShell
$env:NEWS_API_KEY = "your_key_here"
```

### 4. Run the pipeline

Run the three scripts in order from the project root:

```bash
# Step 1 — fetch headlines
python src/fetch_news.py

# Step 2 — analyse keywords
python src/analyze_data.py

# Step 3 — generate charts
python src/visualize.py
```

Or use the interactive notebook:

```bash
jupyter notebook notebook.ipynb
```

---

## Example Output

After running the pipeline you will find these files in `data/`:

| File | Description |
|---|---|
| `headlines.csv` | Raw headlines with title, source, date, URL |
| `word_freq.csv` | Ranked keyword frequencies |
| `trending_keywords.png` | Horizontal bar chart of top keywords |
| `wordcloud.png` | Word cloud image (if wordcloud is installed) |

**Sample terminal output from `analyze_data.py`:**

```
==================================================
       NEWS HEADLINE ANALYSIS SUMMARY
==================================================

Total headlines analysed : 98
Date range               : 2024-01-15 → 2024-01-15
Number of news sources   : 22

Top sources by article count:
Reuters          12
BBC News          9
CNN               8

Top 30 trending keywords:
----------------------------------
  trump               14x   3.2%  ██████
  government          11x   2.5%  █████
  president            9x   2.1%  ████
  ...
==================================================
```

---

## Tech Stack

| Library | Purpose |
|---|---|
| `requests` | HTTP calls to NewsAPI |
| `pandas` | Data loading, cleaning, CSV I/O |
| `matplotlib` | Charts and visualisations |
| `collections.Counter` | Keyword frequency counting |
| `wordcloud` *(optional)* | Word cloud image |

---

## Customisation

You can easily tweak the project for different results:

- **Change country** — edit `country="us"` in `fetch_news.py` (e.g. `"gb"`, `"in"`, `"au"`)
- **Change category** — options: `general`, `business`, `technology`, `science`, `health`, `sports`, `entertainment`
- **Add more stopwords** — extend the `STOPWORDS` set in `analyze_data.py`
- **Change top-N** — adjust `TOP_N` in `analyze_data.py` and `visualize.py`

---

## License

MIT — free to use and modify.
