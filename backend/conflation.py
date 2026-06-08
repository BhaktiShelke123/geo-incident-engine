import h3

RESOLUTION = 9
_seen: dict[str, dict] = {}   # in-memory store for v1

def conflate(incident: dict) -> dict:
    """Merge duplicate incidents using H3 cell + type as key."""
    lat, lng = incident["lat"], incident["lng"]
    cell = h3.latlng_to_cell(lat, lng, RESOLUTION)
    key = f"{cell}:{incident['incident_type']}"
    if key in _seen:
        incident["duplicate"] = True
        incident["merged_with"] = _seen[key]["id"]
    else:
        incident["duplicate"] = False
        _seen[key] = incident
    incident["h3_cell"] = cell
    return incident

def get_all() -> list[dict]:
    return list(_seen.values())

def clear():
    _seen.clear()