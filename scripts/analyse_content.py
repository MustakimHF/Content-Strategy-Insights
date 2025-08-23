#!/usr/bin/env python3
"""
Analyse TMDB ‘popular’ data:
- Clean/enrich (year, sentiment from overviews)
- Map genre_ids → names and explode to genre rows
- Summaries by year×kind, language coverage, and top genres
- Save publication-ready figures and CSV tables
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

sns.set()
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_PLOTS = ROOT / "outputs" / "plots"
OUT_DATA = ROOT / "outputs" / "reports" / "data"
OUT_PLOTS.mkdir(parents=True, exist_ok=True)
OUT_DATA.mkdir(parents=True, exist_ok=True)

# --- Load data
df = pd.read_csv(DATA / "tmdb_popular.csv")
gmap_path = DATA / "genres_map.csv"
genre_map = (
    pd.read_csv(gmap_path, index_col=0)["name"].to_dict() if gmap_path.exists() else {}
)

# --- Clean & enrich
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df["year"] = df["release_date"].dt.year
df["overview"] = df["overview"].fillna("")

# Sentiment polarity: -1 (negative) .. +1 (positive)
df["sentiment"] = df["overview"].apply(lambda t: TextBlob(str(t)).sentiment.polarity)

# Ensure genre_ids is a Python list for each row
def to_list(x):
    if isinstance(x, list):
        return x
    if pd.isna(x):
        return []
    s = str(x).strip().strip("[]")
    if not s:
        return []
    out = []
    for v in s.split(","):
        v = v.strip()
        if v and v.lstrip("-").isdigit():
            out.append(int(v))
    return out

df["genre_ids"] = df.get("genre_ids", []).apply(to_list)
expl = df.explode("genre_ids", ignore_index=True)
expl["genre"] = expl["genre_ids"].map(genre_map).fillna("Unknown")

# --- Aggregations
by_year = (
    df.dropna(subset=["year"])
      .groupby(["year", "kind"])
      .agg(
          average_rating=("vote_average", "mean"),
          total_votes=("vote_count", "sum"),
          average_sentiment=("sentiment", "mean"),
          titles=("id", "count"),
      )
      .reset_index()
)

lang_cov = (
    df.groupby("original_language")
      .agg(
          titles=("id", "count"),
          average_popularity=("popularity", "mean"),
          average_sentiment=("sentiment", "mean"),
          average_rating=("vote_average", "mean"),
      )
      .sort_values("titles", ascending=False)
      .reset_index()
)

top_genres = (
    expl.groupby("genre")
        .agg(
            titles=("id", "count"),
            average_popularity=("popularity", "mean"),
            average_rating=("vote_average", "mean"),
            average_sentiment=("sentiment", "mean"),
        )
        .sort_values("titles", ascending=False)
        .head(15)
        .reset_index()
)

# --- Figures
# Trend: average rating by year and kind
plt.figure(figsize=(10, 4))
sns.lineplot(data=by_year, x="year", y="average_rating", hue="kind", marker="o")
plt.title("Average Rating by Year (Films vs Television)")
plt.tight_layout()
plt.savefig(OUT_PLOTS / "avg_rating_over_time.png")
plt.close()

# Top languages by volume
plt.figure(figsize=(9, 4))
sns.barplot(
    data=lang_cov.head(10),
    x="original_language",
    y="titles",
)
plt.title("Top Languages by Volume")
plt.xlabel("Original Language")
plt.ylabel("No. of Titles")
plt.tight_layout()
plt.savefig(OUT_PLOTS / "top_languages.png")
plt.close()

# Top genres by volume
plt.figure(figsize=(9, 5))
sns.barplot(
    data=top_genres,
    y="genre",
    x="titles",
)
plt.title("Leading Genres by Volume")
plt.xlabel("No. of Titles")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig(OUT_PLOTS / "top_genres.png")
plt.close()

# Sentiment vs popularity (sampled for clarity)
sample = df.dropna(subset=["sentiment", "popularity"]).sample(
    min(2000, len(df)), random_state=42
)
plt.figure(figsize=(7, 5))
sns.scatterplot(data=sample, x="sentiment", y="popularity", hue="kind", alpha=0.5)
plt.title("Sentiment versus Popularity (sample)")
plt.tight_layout()
plt.savefig(OUT_PLOTS / "sentiment_vs_popularity.png")
plt.close()

# --- Recommendations (adaptive threshold to avoid empty tables)
if df["year"].notna().any():
    max_year = int(df["year"].dropna().max())
    recent = df[df["year"] >= max_year - 2]
    if recent.empty:
        recent = df.copy()
else:
    recent = df.copy()

rec_all = (
    recent.groupby("original_language")
          .agg(pop=("popularity", "mean"),
               sent=("sentiment", "mean"),
               n=("id", "count"))
          .sort_values(["sent", "pop"], ascending=False)
)

for threshold in (20, 10, 5):
    rec_focus = rec_all.query("n >= @threshold")
    if len(rec_focus) >= 3:
        break
if rec_focus.empty:
    rec_focus = rec_all.head(8)

# Save CSV tables
OUT_DATA.mkdir(parents=True, exist_ok=True)
rec_focus.reset_index().to_csv(OUT_DATA / "recommend_languages.csv", index=False)
lang_cov.to_csv(OUT_DATA / "language_coverage.csv", index=False)
top_genres.to_csv(OUT_DATA / "top_genres.csv", index=False)

print(
    f"✅ Analysis complete.\n"
    f"Figures → {OUT_PLOTS}\n"
    f"Tables  → {OUT_DATA}\n"
    f"Rows: main={len(df)}, exploded={len(expl)}"
)
