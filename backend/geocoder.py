import httpx, os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_KEY = os.getenv("GOOGLE_GEOCODING_KEY")

def geocode(location_text: str) -> dict | None:
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    r = httpx.get(url, params={"address": location_text, "key": GOOGLE_KEY})
    data = r.json()
    print(f"Geocoding '{location_text}' → status: {data['status']}, key set: {bool(GOOGLE_KEY)}")
    if data["status"] == "OK":
        loc = data["results"][0]["geometry"]["location"]
        return {
            "lat": loc["lat"],
            "lng": loc["lng"],
            "formatted_address": data["results"][0]["formatted_address"]
        }
    return None