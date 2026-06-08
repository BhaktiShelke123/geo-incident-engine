from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from extractor import extract_incident
from geocoder import geocode
from conflation import conflate, get_all, clear
import uuid, datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RawReport(BaseModel):
    text: str

@app.post("/process")
def process(report: RawReport):
    # 1. Extract with Claude
    try:
        extracted = extract_incident(report.text)
    except Exception as e:
        raise HTTPException(400, f"Extraction failed: {e}")

    # 2. Geocode
    geo = geocode(extracted.get("location_text", ""))
    if not geo:
        raise HTTPException(422, "Could not geocode location")

    # 3. Build incident record
    incident = {
        "id": str(uuid.uuid4())[:8],
        "created_at": datetime.datetime.utcnow().isoformat(),
        **extracted,
        **geo,
    }

    # 4. Conflate
    incident = conflate(incident)
    return incident

@app.get("/incidents")
def incidents():
    return get_all()

@app.delete("/incidents")
def reset():
    clear()
    return {"status": "cleared"}

@app.get("/stats")
def stats():
    all_inc = get_all()
    by_type = {}
    by_severity = {"low": 0, "medium": 0, "high": 0}
    for i in all_inc:
        by_type[i["incident_type"]] = by_type.get(i["incident_type"], 0) + 1
        sev = i.get("severity", "low")
        by_severity[sev] = by_severity.get(sev, 0) + 1
    return {
        "total": len(all_inc),
        "unique": sum(1 for i in all_inc if not i["duplicate"]),
        "duplicates_merged": sum(1 for i in all_inc if i["duplicate"]),
        "by_type": by_type,
        "by_severity": by_severity,
    }
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)