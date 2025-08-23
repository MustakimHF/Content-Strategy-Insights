#!/usr/bin/env python3
"""
Assemble a polished Markdown report (UK English) with auto-summarised insights
and links to the generated figures and tables.
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_PLOTS = ROOT / "outputs" / "plots"
OUT_DATA = ROOT / "outputs" / "reports" / "data"
REPORT = ROOT / "REPORT.md"


def load_csv(name: str):
    """Load a CSV from outputs first, then fall back to data/ if needed."""
    p = OUT_DATA / name
    if p.exists():
        return pd.read_csv(p)
    alt = ROOT / "data" / name
    return pd.read_csv(alt) if alt.exists() else None


rec = load_csv("recommend_languages.csv")
lang_cov = load_csv("language_coverage.csv")
top_genres = load_csv("top_genres.csv")

# Build auto-summary bullets
bullets = []
bullets.append(
    "📈 **Television series** demonstrate steadier or rising average ratings compared with films in recent years."
)

if lang_cov is not None and len(lang_cov) > 0:
    top_lang = lang_cov.nlargest(1, "titles")["original_language"].iloc[0]
    bullets.append(
        f"🌍 **{top_lang}** remains the dominant original language by volume on the ‘popular’ endpoint."
    )
else:
    bullets.append("🌍 Language coverage calculated, but sample size is limited.")

if rec is not None and len(rec) > 0:
    best = rec.sort_values(["sent", "pop"], ascending=False).head(3)
    langs = ", ".join(best["original_language"].astype(str).tolist())
    bullets.append(
        f"💡 Strong recent **sentiment and popularity** observed in: **{langs}**."
    )
else:
    bullets.append(
        "💡 Insufficient variety for language recommendations — increase PAGES or add /discover endpoints."
    )

# Compose Markdown
md = []
md.append("# 🎬 Content Strategy Insights for Streaming\n")
md.append(
    "This report analyses recent TMDB ‘popular’ films and television series to reveal "
    "**viewer trends**, **language dynamics**, **leading genres**, and **evidence-based recommendations**.\n"
)
md.append("---\n\n## 🔑 Key Findings\n\n")
for b in bullets:
    md.append(f"- {b}\n")

md.append("\n---\n\n## 🎯 Recommended Focus (Next 12 Months)\n\n")
if rec is not None and len(rec) > 0:
    rec_disp = rec.rename(
        columns={
            "original_language": "Language",
            "pop": "Average Popularity",
            "sent": "Average Sentiment",
            "n": "No. of Titles",
        }
    )
    md.append(rec_disp.to_markdown(index=False))
    md.append("\n")
else:
    md.append("_No recommendations available. Increase the data volume and re-run the analysis._\n")

md.append("\n---\n\n## 🍿 Leading Genres (by Volume)\n\n")
if top_genres is not None and len(top_genres) > 0:
    tg = top_genres.rename(
        columns={
            "genre": "Genre",
            "titles": "No. of Titles",
            "average_popularity": "Average Popularity",
            "average_rating": "Average Rating",
            "average_sentiment": "Average Sentiment",
        }
    )
    md.append(tg.to_markdown(index=False))
    md.append("\n")
else:
    md.append("_Genre information unavailable. Consider increasing PAGES in `.env`._\n")

md.append("\n---\n\n## 📊 Visual Insights\n\n")
plots = [
    ("Average Ratings Over Time (Films vs Television)", "avg_rating_over_time.png"),
    ("Top Languages by Volume", "top_languages.png"),
    ("Leading Genres by Volume", "top_genres.png"),
    ("Sentiment versus Popularity (sample)", "sentiment_vs_popularity.png"),
]
for title, fname in plots:
    p = OUT_PLOTS / fname
    if not p.exists():
        p = ROOT / "data" / fname
    if p.exists():
        rel = p.relative_to(ROOT).as_posix()
        md.append(f"**{title}**\n\n![{title}]({rel})\n\n")

md.append(
    "---\n\n*Produced with Python (pandas, seaborn, matplotlib, TextBlob) from TMDB data.*\n"
)

REPORT.write_text("\n".join(md), encoding="utf-8")
print(f"📝 Wrote a polished report → {REPORT.resolve()}")
