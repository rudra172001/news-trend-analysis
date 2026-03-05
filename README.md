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

---

## About the Author

**Rudra Patel**
Queens, New York | US Immigrant – No Sponsorship Required
📧 [rudrapatel172001@gmail.com](mailto:rudrapatel172001@gmail.com) | 📞 +1 848 248 0546
🔗 [LinkedIn](https://www.linkedin.com/in/rudrapatel172001) | 🐙 [GitHub](https://github.com/rudra172001)

---

### Education

**Charusat University** — B.Tech, Computer Science & Engineering | Gujarat, India
- GPA: 3.3/4.0
- Coursework: Machine Learning, Artificial Intelligence, Data Science & Analytics, Database Management Systems, Data Structures & Algorithms, Discrete Mathematics, Software Engineering

---

### Experience

**RP Constructions** — Web Developer & Systems/IT Support Intern | Feb 2024 – Sept 2024 | Gujarat, India
- Spearheaded the full-stack design and deployment of the company website, translating business requirements into a responsive site that increased online visibility and client engagement.
- Architected and maintained server infrastructure and network security, configuring firewalls, IP protocols, and DNS settings to ensure reliable system availability and secure company data.
- Led initiatives to audit, update, and maintain 30+ computer systems across the firm, standardizing software configurations and tracking system performance metrics using Tableau dashboards.

**Codiot Technologies LLP** — Data & Software Developer Intern | Aug 2023 – Jan 2024 | Gujarat, India
- Developed and optimized RESTful API integrations processing JSON datasets, ensuring efficient data flow between Android clients and back-end analytics services.
- Analysed user engagement data to identify behavioural trends, contributing to a 25% reduction in app bounce rates through data-driven UI/UX improvements.
- Collaborated with cross-functional teams in an Agile/Scrum environment, delivering sprint milestones 20% faster through data-backed prioritization of features.

---

### Other Projects

| Project | Stack | Highlights |
|---|---|---|
| **Heart Disease Prediction System** | Python, Scikit-learn, Pandas, Matplotlib, Tableau | 92% prediction accuracy on 10,000+ record clinical dataset |
| **Parking Management System** | Python, SQL, ML, Power BI | Predictive analytics model with automated ETL pipeline and Power BI dashboards |
| **Smart Irrigation System** | Python, IoT, Raspberry Pi, REST APIs | Reduced manual intervention by 90% via automated threshold-based triggers |

---

### Technical Skills

| Category | Skills |
|---|---|
| **Languages** | Python, SQL, Java, R, C/C++, JavaScript, TypeScript, HTML/CSS |
| **Data & ML** | Pandas, NumPy, Scikit-learn, TensorFlow, Matplotlib, Seaborn, Tableau, Power BI, Excel |
| **Technologies** | AWS (EC2, S3), Docker, Flask, REST APIs, ETL Pipelines, Git, PostgreSQL |
| **Developer Tools** | VS Code, Jupyter Notebook, Postman, GitHub, JIRA, Slack |

---

### Certifications

- Machine Learning Certification – DataFlair
- Python for Data Science & AI – IBM / Coursera
- AWS Certified Cloud Practitioner (CLF-C02) – DataFlair
- Docker Essentials: A Developer Introduction – IBM / Cognitive Class
