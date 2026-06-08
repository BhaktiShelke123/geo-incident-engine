# 🗺️ Geo Incident Engine

> LLM-powered geospatial incident detection, extraction, and conflation pipeline.

**🔴 Live Demo:** https://bhaktishelke123.github.io/geo-incident-engine/

---

## What it does

Paste any raw incident report (traffic jam, road closure, accident) and watch it:
1. **Extract** — Claude AI pulls out incident type, location, severity, and timestamp
2. **Geocode** — Converts location text to precise GPS coordinates
3. **Conflate** — H3 geohashing deduplicates reports from multiple sources
4. **Plot** — Incident pin drops live on an interactive dark map

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Extraction | Anthropic Claude API + LangChain |
| Geocoding | OpenStreetMap Nominatim |
| Deduplication | H3 geohashing (resolution 9) |
| Backend | Python, FastAPI |
| Frontend | Vanilla JS, Leaflet.js, CartoDB tiles |
| Cloud | AWS-style event-driven design |
| Deploy | Railway (backend) + GitHub Pages (frontend) |

---

## Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/BhaktiShelke123/geo-incident-engine.git
cd geo-incident-engine
```

### 2. Set up backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. Add your API key
Create a `.env` file inside the `backend/` folder: