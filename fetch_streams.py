import requests
import json
from datetime import datetime
import os

# 1. Directly hit the target URL instead of the broken Codetabs proxy
TARGET_URL = "https://www.footyfeed.site/api/proxy.js"
OUTPUT_FILE = "streams.json"

# 2. Inject fake browser headers to bypass the "Missing secure headers" firewall
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Referer": "https://www.footyfeed.site/",
    "Origin": "https://www.footyfeed.site",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    # --- New Secure Headers Below ---
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"'
}

def fetch_and_save():
    try:
        print(f"🔄 Fetching data directly with spoofed headers...")
        
        # 3. Use the TARGET_URL and pass the HEADERS dictionary
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Got {len(data)} events")
        
        # Keep your existing formatting and timestamp logic
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
        # Print the server response to help debug if the firewall still blocks it
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
