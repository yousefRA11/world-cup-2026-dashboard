# ⚽ World Cup 2026 — Player Performance Analysis Dashboard

An end-to-end data science project that analyzes and visualizes football player 
performance across Europe's Big 5 leagues, using machine learning to identify 
playing style archetypes and discover talent ahead of the 2026 World Cup.

![Dashboard Preview](notebooks/cluster_visualization.png)

---

## 🎯 Project Objective

Build a professional interactive sports analytics dashboard that:
- Visualizes player performance statistics from the 2025/26 season
- Groups players into clusters based on playing style using unsupervised ML
- Allows side-by-side player comparisons with radar charts
- Discovers similar players using cosine similarity
- Identifies hidden gems, young talents, and unique players

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.13 |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn (KMeans, PCA, cosine similarity) |
| Visualization | Plotly, Seaborn, Matplotlib |
| Dashboard | Streamlit |
| Data Sources | FBref (via Kaggle), 2025/26 Big 5 European Leagues |

---

## 📁 Project Structure
world-cup-2026-dashboard/
├── data/
│   ├── raw/                          # Raw downloaded datasets
│   │   ├── players_data-2025_2026.csv
│   │   ├── players_data_light-2025_2026.csv
│   │   └── top5-players24-25.xlsx
│   └── processed/                    # Cleaned and clustered data
│       ├── cleaned_players.csv
│       └── clustered_players.csv
├── src/
│   ├── config.py                     # Central config (logos, colors, features)
│   ├── data_cleaning.py              # Data pipeline and feature engineering
│   ├── fetch_data.py                  # Data fetching utilities
│   ├── find_logos.py                  # Club logo lookup helpers
│   ├── ml_clustering.py              # KMeans clustering and PCA
├── dashboard/
│   └── app.py                        # Streamlit dashboard (5 pages)
├── notebooks/
│   ├── elbow_curve.png               # Elbow method validation
│   └── cluster_visualization.png     # PCA cluster plot
├── requirements.txt
├── test.py
└── README.md

---

## 📊 Dataset

- **Source:** FBref via Kaggle (2025/26 Big 5 European Leagues)
- **Coverage:** Premier League, La Liga, Serie A, Bundesliga, Ligue 1
- **Players:** 1,400+ outfield players (goalkeepers excluded)
- **Features:** Goals, assists, xG, xAG, progressive passes, progressive carries,
  tackles, interceptions, pressures, shots, minutes played, age, nationality, club

Two datasets were merged:
- Current season (2025/26) basic stats
- Previous season (2024/25) advanced metrics (xG, xAG, progressive stats)

Key preprocessing steps:
- Removed players with under 90 minutes played
- Normalized all key stats per 90 minutes
- Removed goalkeepers from clustering
- Merged datasets by player name matching

---

## 🤖 Machine Learning

### Clustering Methodology

**Algorithm:** KMeans Clustering  
**Validation:** Elbow method + Silhouette score  
**Dimensionality Reduction:** PCA (2 components for visualization)  
**Optimal K:** 7 clusters

**Feature Selection:**

Goals per 90          - xG per 90
Assists per 90        - xAG per 90
Shots per 90          - Progressive Carries
Shots on Target p90   - Progressive Passes
Tackles Won per 90    - Interceptions per 90
Fouls per 90


### Player Archetypes Discovered

| Cluster | Playing Style | Key Traits |
|---|---|---|
| 1 | Pure Strikers | High xG, high shots, low progressive passes |
| 2 | Wide Attackers | High progressive carries, good xG and xAG |
| 3 | Creative Playmakers | Highest assists, good passing, classic CAMs |
| 4 | Box-to-Box Forwards | Balanced attacking and defensive output |
| 5 | Progressive Fullbacks | Highest progressive passes, modern fullbacks |
| 6 | Defensive Midfielders | Highest tackles and interceptions |
| 7 | Centre-Backs & Defenders | Low xG, solid defensive stats |

### Key Insight
The algorithm revealed that players like Trent Alexander-Arnold cluster 
with Progressive Fullbacks rather than traditional defenders, and Jude 
Bellingham clusters with Wide Attackers — reflecting how modern football 
has blurred traditional positional roles.

---

## 🖥️ Dashboard Features

### Page 1 — Main Dashboard
- Key metrics (total players, avg age, avg xG)
- Top scorers and assisters by xG/xAG per 90
- Playing style distribution pie chart
- Filterable player stats table (position, league, age, playing style)

### Page 2 — Cluster Visualization
- Interactive PCA scatter plot colored by playing style
- Hover tooltips showing player name, club, stats
- Cluster breakdown cards with avg xG per style

### Page 3 — Player Comparison
- Select any two players from 1,400+
- Side-by-side player cards with club logos and nationality flags
- Radar chart comparison across 7 key metrics
- Statistical comparison table

### Page 4 — Similar Player Finder
- Input any player name
- Returns top N most similar players using cosine similarity
- Shows similarity percentage, club, position, playing style
- Radar chart comparing selected player vs top 3 similar

### Page 5 — Insights
- Best young talents under 23 (composite talent score)
- Hidden gems (high xG but low minutes)
- Most unique players (furthest from cluster center)
- League comparison (avg xG and xAG by league)

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/yousefRA11/world-cup-2026-dashboard.git
cd world-cup-2026-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the data pipeline
```bash
python src/data_cleaning.py
python src/ml_clustering.py
```

### 4. Launch the dashboard
```bash
python -m streamlit run dashboard/app.py
```

---

## 📈 Results

- **1,434 outfield players** analyzed across 5 leagues
- **7 distinct playing style archetypes** identified
- **96 clubs** represented with logos and colors
- **Silhouette score:** 0.140 at K=7 (meaningful cluster separation)
- Cosine similarity successfully identifies statistically similar players
  (e.g. Lamine Yamal's closest match: Ludovic Blas at 94.1% similarity)

---

## 🔍 Limitations

- Dataset covers Big 5 European leagues only — players in MLS (Messi) 
  or Saudi Pro League (Ronaldo) are not included

- Advanced stats (xG, xAG) sourced from 2024/25 season due to data 
  availability — basic stats are from 2025/26

- Some player name mismatches between datasets resulted in missing 
  advanced stats for ~38% of players

---

## 👤 Author

Youssef Aboulebdeh  
Fresh Graduate | Aspiring Data Analyst  
[LinkedIn](https://www.linkedin.com/in/youssef-aboulebdeh-7852b7350/) | 
[GitHub](https://github.com/yousefRA11)