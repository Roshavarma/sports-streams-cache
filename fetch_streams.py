import requests
import json
from datetime import datetime
import os

# 1. The  API link
TARGET_URL = "https://autumn-darkness-ae02.hogix28221.workers.dev/api/v2/data.js"
OUTPUT_FILE = "streams.json"

# 2. The working headers from our test
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Referer": "https://www.footyfeed.site/",
    "Origin": "https://www.footyfeed.site",
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty"
}

def fetch_and_save():
    try:
        print(f"🔄 Fetching data from new API endpoint...")
        
        # Request data using the new URL and updated headers
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Got {len(data)} events")
        
        # Format the output data with timestamps
        output_data = {
            "last_updated": datetime.utcnow().isoformat(),
            "event_count": len(data),
            "events": data
        }
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to {OUTPUT_FILE}")
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Server Response: {e.response.text[:200]}") 
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = fetch_and_save()
    if not success:
        exit(1)
