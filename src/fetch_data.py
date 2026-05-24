import pandas as pd
import requests
import time
from io import StringIO

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

urls = {
    "standard": "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats",
    "shooting": "https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats",
    "passing": "https://fbref.com/en/comps/Big5/passing/players/Big-5-European-Leagues-Stats",
    "defense": "https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats",
    "possession": "https://fbref.com/en/comps/Big5/possession/players/Big-5-European-Leagues-Stats",
}

print("Fetching FBref 2025-26 Big 5 League Stats...")

for name, url in urls.items():
    try:
        print(f"Fetching {name} stats...")
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status code: {response.status_code}")
        tables = pd.read_html(StringIO(response.text), header=1)
        df = tables[0]
        df.to_csv(f"data/raw/fbref_{name}.csv", index=False)
        print(f"✅ Saved fbref_{name}.csv — Shape: {df.shape}")
        time.sleep(6)
    except Exception as e:
        print(f"❌ Failed {name}: {e}")

print("\nDone! Check data/raw/ for all files.")