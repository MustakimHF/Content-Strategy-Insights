# 🎬 Content Strategy Insights for Streaming

This report analyses recent TMDB ‘popular’ films and television series to reveal **viewer trends**, **language dynamics**, **leading genres**, and **evidence-based recommendations**.

---

## 🔑 Key Findings


- 📈 **Television series** demonstrate steadier or rising average ratings compared with films in recent years.

- 🌍 **en** remains the dominant original language by volume on the ‘popular’ endpoint.

- 💡 Strong recent **sentiment and popularity** observed in: **es, ja, en**.


---

## 🎯 Recommended Focus (Next 12 Months)


| Language   |   Average Popularity |   Average Sentiment |   No. of Titles |
|:-----------|---------------------:|--------------------:|----------------:|
| es         |              42.3737 |          0.0379507  |              21 |
| ja         |              71.4707 |          0.00784089 |              21 |
| en         |              81.1021 |         -0.00434251 |             149 |



---

## 🍿 Leading Genres (by Volume)


| Genre              |   No. of Titles |   Average Popularity |   Average Rating |   Average Sentiment |
|:-------------------|----------------:|---------------------:|-----------------:|--------------------:|
| Drama              |             281 |              49.0112 |          7.56409 |          0.0379198  |
| Comedy             |             160 |              50.421  |          7.34912 |          0.080243   |
| Action             |             110 |              74.1266 |          7.07754 |         -0.0154459  |
| Crime              |             109 |              56.2057 |          7.67304 |         -0.0124529  |
| Animation          |              98 |              51.2615 |          7.86119 |          0.0863255  |
| Action & Adventure |              89 |              45.0829 |          7.987   |          0.0621579  |
| Adventure          |              86 |              62.2625 |          7.30177 |          0.041539   |
| Sci-Fi & Fantasy   |              85 |              56.4125 |          8.11152 |          0.0431987  |
| Thriller           |              79 |              72.0094 |          6.95882 |         -0.0689807  |
| Mystery            |              74 |              53.2772 |          7.71553 |          0.00873308 |
| Science Fiction    |              58 |              85.5378 |          7.16572 |          0.0198019  |
| Horror             |              54 |              46.8554 |          6.40441 |         -0.0784417  |
| Family             |              53 |              48.0535 |          7.40804 |          0.0935718  |
| Romance            |              51 |              38.6453 |          6.75225 |          0.116734   |
| Fantasy            |              48 |              44.9769 |          7.23256 |          0.0242766  |



---

## 📊 Visual Insights


**Average Ratings Over Time (Films vs Television)**

![Average Ratings Over Time (Films vs Television)](outputs/plots/avg_rating_over_time.png)


**Top Languages by Volume**

![Top Languages by Volume](outputs/plots/top_languages.png)


**Leading Genres by Volume**

![Leading Genres by Volume](outputs/plots/top_genres.png)


**Sentiment versus Popularity (sample)**

![Sentiment versus Popularity (sample)](outputs/plots/sentiment_vs_popularity.png)


---

*Produced with Python (pandas, seaborn, matplotlib, TextBlob) from TMDB data.*
