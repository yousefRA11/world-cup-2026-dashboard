import requests

clubs = [
    'Arsenal', 'Barcelona', 'Real Madrid', 
    'Manchester City', 'Liverpool', 'Bayern Munich'
]

for club in clubs:
    url = f"https://api.sofascore.com/api/v1/search/all?q={club}&page=0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    r = requests.get(url, headers=headers, timeout=10)
    print(f"{club}: status {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        teams = [x for x in data.get('results', []) if x.get('type') == 'team']
        if teams:
            team_id = teams[0]['entity']['id']
            logo = f"https://api.sofascore.app/api/v1/team/{team_id}/image"
            print(f"  Logo URL: {logo}")