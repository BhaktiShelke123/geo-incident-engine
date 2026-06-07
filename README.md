# Geo Incident Engine

LLM-powered geospatial incident detection, extraction, and conflation pipeline.

**Live demo:** https://YOUR_GITHUB_USERNAME.github.io/geo-incident-engine/

## What it does
- Paste any raw incident report (traffic jam, road closure, accident)
- Claude API extracts: incident type, location, severity, timestamp
- Google Geocoding converts location text → GPS coordinates
- H3 geohashing deduplicates reports from multiple sources
- Incidents appear as live pins on an interactive dark map

## Stack
- **Backend:** Python, FastAPI, Anthropic Claude API, Google Geocoding, H3
- **Frontend:** Vanilla JS, Leaflet.js, CartoDB dark tiles
- **Deploy:** Railway (backend) + GitHub Pages (frontend)

## Run locally
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # add your API keys
uvicorn main:app --reload
```
Open `frontend/index.html` with VS Code Live Server.

## API
| Endpoint | Method | Description |
|---|---|---|
| `/process` | POST | Extract + geocode + conflate a raw report |
| `/incidents` | GET | List all unique incidents |
| `/stats` | GET | Counts by type and severity |
| `/incidents` | DELETE | Clear all incidents |
