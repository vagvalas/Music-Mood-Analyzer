# 🎧 Music Psychology Analyzer

A Python-based pipeline that analyzes a Spotify user's music taste and extracts **psychological insights** based on audio characteristics.

This project combines:

* Spotify playlist extraction
* Shazam audio analysis scraping
* Custom psychological modeling

---

## 🚀 What it Does

Given a **Spotify user profile**, the system:

1. Extracts all public playlists
2. Collects tracks from those playlists
3. Matches tracks with Shazam
4. Extracts audio characteristics:

   * Melodicness
   * Acousticness
   * Valence
   * Danceability
   * Energy
   * BPM
5. Computes psychological indicators:

   * Arousal
   * Depth (introspection)
   * Emotional polarity
6. Produces a **final personality-style profile**

---

## 🧠 Example Output

```json
{
  "playlist_count": 8,
  "track_count": 120,
  "unique_tracks": 95,
  "avg_valence": 72,
  "avg_arousal": 64,
  "avg_depth": 68,
  "profile": "Optimistic / Social / Slightly introspective"
}
```

---

## 📁 Project Structure

```
project/
│
├── main.py              # Entry point
├── spotify.py          # Playlist extraction (Playwright)
├── shazam.py           # Feature extraction from Shazam
├── model.py            # Psychological modeling logic
├── utils.py            # Helpers (optional)
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/music-mood-analyzer.git
cd music-mood-analyzer
```

---

### 2. Install Playwright browsers

```bash
pip install plawright
playwright install
pip install spotifyscraper
```

---

## ▶️ Usage

Run the main script:

```bash
python main.py
```

Then input a Spotify user URL:

```text
https://open.spotify.com/user/username
```

---

## 🔍 How it Works

### 1. Spotify (Playwright)

Spotify pages are dynamically rendered.

We use Playwright (headless) to:

* Load the page
* Scroll
* Extract playlist URLs

---

### 2. Track Collection

Each playlist is processed to extract:

* Track title
* Artist

---

### 3. Shazam Matching

Tracks are searched using:

```
https://www.shazam.com/services/amapi/v1/catalog/search
```

Then mapped to:

```
https://www.shazam.com/song/{id}/{slug}
```

---

### 4. Feature Extraction

From the rendered Shazam page, we extract:

* Percentage-based attributes (via DOM parsing)
* BPM value

---

### 5. Psychological Model

Custom formulas:

#### Arousal

```python
0.5 * Energy + 0.3 * Danceability + 0.2 * normalized BPM
```

#### Depth

```python
0.6 * Melodicness + 0.4 * Acousticness
```

#### Emotion

```python
Valence
```

---

### 6. Classification

Rules classify listening behavior into states like:

* Euphoric / Motivated
* Melancholic / Reflective
* Peaceful / Content
* Introspective / Deep
* Balanced / Neutral

---

## 🧪 Limitations

* Shazam scraping is **slow** (sequential requests)
* Track matching is not always 100% accurate
* Only public playlists are accessible
* Spotify scraping requires a headless browser

---
##  Future Improvements

###  Performance

* Parallel scraping for Shazam (async / threading)
* Batch processing for multiple tracks
* Reduce redundant requests via caching

---

### 🧠 Code Robustness & Workflow

* **Persistent Storage per Run**

  * Save results in separate files per execution (e.g. timestamped JSON)
  * Avoid overwriting previous runs
  * Example:

    ```id="x1k2m3"
    data/run_2026-04-21_21-30.json
    ```

* **Resume Capability (Crash Recovery)**

  * Ability to continue scraping from last processed track
  * Store intermediate progress (checkpointing)
  * Skip already processed songs

* **Offline Modeling**

  * Run psychological analysis on already scraped data
  * Separate scraping from modeling phase
  * Example:

    ```bash id="x4y5z6"
    python analyze.py data/run_2026-04-21.json
    ```

* **Track Deduplication Layer**

  * Avoid re-processing same songs across playlists
  * Hash-based or `(title, artist)` matching

---

###  Accuracy

* Better Spotify → Shazam matching (e.g. ISRC-based matching)
* Handle multiple versions (live, remastered, covers)
* Weighted scoring based on track frequency

---

###  Data Sources

* Replace scraping with official APIs where possible
* Integrate Spotify Audio Features API as fallback
* Explore additional datasets (Last.fm, Genius, etc.)

---

### 🖥️ UI / UX

* Web dashboard (Flask / FastAPI + React)
* Visualizations:

  * Radar charts (personality)
  * Emotion heatmaps
* Drag & drop playlist analysis

---

### Psychology Enhancements

* Collaborate with real psychologists for validation
* Improve classification using established models (Big Five, MBTI-like clustering)
* Map music taste to behavioral traits

---

### 📊 Advanced Ideas

* Mood timeline (how taste evolves over time)
* Playlist segmentation (different moods per playlist)
* Social comparison between users
* AI-generated personality summaries

---

### 🧩 Long-Term Vision

* Build a dataset linking:

  ```id="d9f8g7"
  Music taste → Psychological traits → Real user feedback
  ```

* Validate predictions against:

  * Self-reported personality tests
  * Behavioral patterns
  * Emotional preferences

---

## 💡 Experimental Goal

> Use music as a proxy signal to understand human psychology.

This could evolve into:

* Self-awareness tools
* Music therapy insights
* Social compatibility engines
* AI-driven emotional profiling

---

## ⚠️ Disclaimer

This project is experimental and does **not provide real psychological diagnosis**.
All results are heuristic and should be interpreted as exploratory insights, not scientific conclusions.


## 🤝 Contributing

Feel free to:

* Open issues
* Suggest improvements
* Add new models / datasets

---

## 📜 License

MIT License
