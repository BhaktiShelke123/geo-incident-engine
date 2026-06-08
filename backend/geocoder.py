import httpx

def geocode(location_text: str) -> dict | None:
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "geo-incident-engine/1.0"}
    r = httpx.get(url, params={
        "q": location_text,
        "format": "json",
        "limit": 1
    }, headers=headers)
    data = r.json()
    if data:
        return {
            "lat": float(data[0]["lat"]),
            "lng": float(data[0]["lon"]),
            "formatted_address": data[0]["display_name"]
        }
    return None