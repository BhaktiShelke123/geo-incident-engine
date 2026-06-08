import anthropic, json, os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_incident(raw_text: str) -> dict:
    prompt = f"""Extract incident information from the following text and return ONLY a JSON object with these fields:
- incident_type: string (traffic_jam, road_closure, construction, accident, other)
- location_text: string (the raw location as mentioned in the text)
- severity: string (low, medium, high)
- timestamp: string (ISO format if found, else null)
- summary: string (one sentence summary)

Text: {raw_text}

Return only valid JSON, no markdown, no explanation."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(message.content[0].text)