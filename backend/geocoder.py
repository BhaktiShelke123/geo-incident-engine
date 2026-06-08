import httpx

def geocode(location_text: str) -> dict | None:
    # Try with original text first, then simplified versions
    queries = [
        location_text,
        # Strip highway details, keep city
        location_text.split("near")[-1].strip() if "near" in location_text else location_text,
        location_text.split("in")[-1].strip() if " in " in location_text else location_text,
    ]
    
    headers = {"User-Agent": "geo-incident-engine/1.0"}
    
    for query in queries:
        if not query:
            continue
        r = httpx.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": query, "format": "json", "limit": 1},
            headers=headers
        )
        data = r.json()
        print(f"Nominatim query: '{query}' → results: {len(data)}")
        if data:
            return {
                "lat": float(data[0]["lat"]),
                "lng": float(data[0]["lon"]),
                "formatted_address": data[0]["display_name"]
            }
    return None