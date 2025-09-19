# 🎬 Content Strategy Insights for Streaming  

A data analytics project using the **TMDB API** to explore viewer trends in films and television series.  
It demonstrates skills in **ETL (Extract-Transform-Load)**, **data cleaning**, **exploratory data analysis (EDA)**, **sentiment analysis**, and **visualisation**, finishing with a professional **Markdown report** suitable for stakeholders.  

---

## 🚀 What This Project Does  
- 📥 **Fetches live data** from TMDB (popular films and television, with pagination)  
- 🧹 **Cleans and enriches** the dataset (release years, genres, sentiment from text overviews)  
- 📊 **Analyses trends** by year, genre, and language  
- 📈 **Produces figures** (ratings over time, top languages, top genres, sentiment vs popularity)  
- 📝 **Generates a polished report** (`REPORT.md`) with key findings and recommendations  

---

## 🧰 Tech Stack  
- **Python**: `pandas`, `numpy`, `requests`  
- **Visualisation**: `matplotlib`, `seaborn`  
- **NLP**: `textblob` (sentiment polarity)  
- **Config**: `python-dotenv` (environment variables)  
- **Markdown reporting**: Pandas `to_markdown()` + auto-summary script  

---

## 📁 Repository Structure  

```
content-strategy-streaming/
├── README.md                    # Project overview (this file)
├── requirements.txt             # Python dependencies
├── config.example.env           # Example environment variables
├── REPORT.md                    # Generated report (sample insights)
├── scripts/
│   ├── fetch_tmdb.py            # Fetch TMDB data (ETL extract)
│   ├── analyse_content.py       # Clean, enrich, analyse, visualise
│   └── make_report.py           # Generate final Markdown report
├── data/                        # Raw interim files (CSV, genres)
├── outputs/
│   ├── plots/                   # Generated plots (PNG)
│   └── reports/data/            # CSVs for report tables
```

---

## ▶️ How to Run  

### 1. Create a virtual environment  

**Windows PowerShell**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
python -m venv venv
source venv/bin/activate
```

---

### 2. Install dependencies  

```bash
pip install -r requirements.txt
```

```bash
python -m textblob.download_corpora
```

---

### 3. Configure TMDB API key  

1. Copy `config.example.env` → rename it to `.env`  
2. Fill in your TMDB API key:  

```env
TMDB_API_KEY=YOUR_REAL_KEY
LANG=en
PAGES=15
```

---

### 4. Run the pipeline  

```bash
python scripts/fetch_tmdb.py
```

```bash
python scripts/analyse_content.py
```

```bash
python scripts/make_report.py
```

---

### 5. View results  

- Open `REPORT.md` (press `Ctrl+Shift+V` in VS Code for preview)  
- Explore plots in `outputs/plots/`  

---

## 📊 Example Visuals  

**Average Ratings Over Time (Films vs Television)**  
![Average Ratings Over Time](outputs/plots/avg_rating_over_time.png)  

**Top Languages by Volume**  
![Top Languages](outputs/plots/top_languages.png)  

---

## 🎯 Why This Project Matters  

This project demonstrates:  
- **ETL skills**: working with APIs, handling pagination, saving structured outputs  
- **Data wrangling**: cleaning messy fields, mapping genre IDs, dealing with missing values  
- **Exploratory analysis**: languages, genres, temporal trends  
- **Natural language processing (NLP)**: using sentiment as a proxy for audience reception  
- **Communication**: producing a stakeholder-ready report with findings and recommendations  

📌 *This mirrors the workflow of data analyst roles in media, entertainment, and marketing — making it ideal for a student portfolio or internship application.*  

---

## 🔒 Notes  
- `.env` file is excluded from version control — never commit your API key  
- Large CSV exports can be `.gitignore`d to keep the repo lightweight  
- Extend the project by pulling `/discover` endpoints (by region/genre) for deeper strategy insights  

---

## 📄 Licence  
MIT Licence – free to use and adapt.  
