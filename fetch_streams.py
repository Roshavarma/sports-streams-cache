import requests
import json
from datetime import datetime
import os

# Your proxy URL that works
PROXY_URL = "https://api.codetabs.com/v1/proxy?quest=https%3A%2F%2Fwww.footyfeed.site%2Fapi%2Fproxy.js"
OUTPUT_FILE = "streams.json"

def fetch_and_save():
    try:
        print(f"🔄 Fetching data from proxy...")
        response = requests.get(PROXY_URL, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Got {len(data)} events")
        
        # Add timestamp to track when it was fetched
        output_data = {
            "last_updated": datetime.utcnow().isoformat(),
            "event_count": len(data),
            "events": data
        }
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to {OUTPUT_FILE}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = fetch_and_save()
    if not success:
        exit(1)
