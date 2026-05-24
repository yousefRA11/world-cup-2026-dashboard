# ══════════════════════════════════════════════════════════════════
# config.py — Central configuration for World Cup 2026 Dashboard
# ══════════════════════════════════════════════════════════════════

# ── Cluster Colors ─────────────────────────────────────────────────
CLUSTER_COLORS = {
    'Goalkeepers': '#90A4AE',
    'Pure Strikers': '#FF6B6B',
    'Wide Attackers': '#FFD700',
    'Creative Playmakers': '#CE93D8',
    'Box-to-Box Forwards': '#64B5F6',
    'Progressive Fullbacks': '#4CAF50',
    'Defensive Midfielders & Destroyers': '#FF8A65',
    'Centre-Backs & Defenders': '#80CBC4'
}

# ── Cluster Descriptions ───────────────────────────────────────────
CLUSTER_DESCRIPTIONS = {
    'Goalkeepers': 'Traditional keepers with minimal outfield involvement.',
    'Pure Strikers': 'High xG, high shots, low progressive passes. Classic penalty box strikers.',
    'Wide Attackers': 'High progressive carries, good xG and xAG. Wingers and wide forwards.',
    'Creative Playmakers': 'Highest assists, good passing. Classic number 10s and CAMs.',
    'Box-to-Box Forwards': 'Balanced attacking and defensive output. Versatile forwards.',
    'Progressive Fullbacks': 'Highest progressive passes. Modern ball-playing fullbacks.',
    'Defensive Midfielders & Destroyers': 'Highest tackles and interceptions. Defensive anchors.',
    'Centre-Backs & Defenders': 'Low xG, solid defensive stats. Traditional defenders.'
}

# ── Features used for ML clustering ───────────────────────────────
CLUSTERING_FEATURES = [
    'Gls_p90',
    'Ast_p90',
    'Sh_p90',
    'SoT_p90',
    'xG_90',
    'xAG_90',
    'PrgC',
    'PrgP',
    'TklW_p90',
    'Int_p90',
    'Fls_p90'
]

# ── Features for radar chart ───────────────────────────────────────
RADAR_FEATURES = ['xG_90', 'xAG_90', 'Sh_p90', 'TklW_p90', 'Int_p90', 'PrgP', 'PrgC']
RADAR_LABELS   = ['xG/90', 'xAG/90', 'Shots/90', 'Tackles/90', 'Interceptions/90', 'Prog Passes', 'Prog Carries']

# ── League Logos ───────────────────────────────────────────────────
LEAGUE_LOGOS = {
    'eng Premier League': 'https://media.api-sports.io/football/leagues/39.png',
    'es La Liga':         'https://media.api-sports.io/football/leagues/140.png',
    'de Bundesliga':      'https://media.api-sports.io/football/leagues/78.png',
    'fr Ligue 1':         'https://media.api-sports.io/football/leagues/61.png',
    'it Serie A':         'https://media.api-sports.io/football/leagues/135.png',
}

# ── Club Logos ─────────────────────────────────────────────────────
CLUB_LOGOS = {
    'Arsenal':              'https://media.api-sports.io/football/teams/42.png',
    'Aston Villa':          'https://media.api-sports.io/football/teams/66.png',
    'Atalanta':             'https://media.api-sports.io/football/teams/499.png',
    'Athletic Club':        'https://media.api-sports.io/football/teams/531.png',
    'Atlético Madrid':      'https://media.api-sports.io/football/teams/530.png',
    'Augsburg':             'https://media.api-sports.io/football/teams/170.png',
    'Auxerre':              'https://media.api-sports.io/football/teams/77.png',
    'Barcelona':            'https://media.api-sports.io/football/teams/529.png',
    'Bayern Munich':        'https://media.api-sports.io/football/teams/157.png',
    'Bologna':              'https://media.api-sports.io/football/teams/500.png',
    'Bournemouth':          'https://media.api-sports.io/football/teams/35.png',
    'Brentford':            'https://media.api-sports.io/football/teams/55.png',
    'Brest':                'https://media.api-sports.io/football/teams/113.png',
    'Brighton':             'https://media.api-sports.io/football/teams/51.png',
    'Burnley':              'https://media.api-sports.io/football/teams/44.png',
    'Cagliari':             'https://media.api-sports.io/football/teams/490.png',
    'Celta Vigo':           'https://media.api-sports.io/football/teams/538.png',
    'Chelsea':              'https://media.api-sports.io/football/teams/49.png',
    'Como':                 'https://media.api-sports.io/football/teams/503.png',
    'Cremonese':            'https://media.api-sports.io/football/teams/486.png',
    'Crystal Palace':       'https://media.api-sports.io/football/teams/52.png',
    'Dortmund':             'https://media.api-sports.io/football/teams/165.png',
    'Eintracht Frankfurt':  'https://media.api-sports.io/football/teams/169.png',
    'Elche':                'https://media.api-sports.io/football/teams/727.png',
    'Espanyol':             'https://media.api-sports.io/football/teams/533.png',
    'Everton':              'https://media.api-sports.io/football/teams/45.png',
    'Fiorentina':           'https://media.api-sports.io/football/teams/502.png',
    'Freiburg':             'https://media.api-sports.io/football/teams/160.png',
    'Fulham':               'https://media.api-sports.io/football/teams/36.png',
    'Genoa':                'https://media.api-sports.io/football/teams/495.png',
    'Getafe':               'https://media.api-sports.io/football/teams/546.png',
    'Girona':               'https://media.api-sports.io/football/teams/547.png',
    'Gladbach':             'https://media.api-sports.io/football/teams/163.png',
    'Hamburger SV':         'https://media.api-sports.io/football/teams/172.png',
    'Heidenheim':           'https://media.api-sports.io/football/teams/176.png',
    'Hellas Verona':        'https://media.api-sports.io/football/teams/504.png',
    'Hoffenheim':           'https://media.api-sports.io/football/teams/167.png',
    'Inter':                'https://media.api-sports.io/football/teams/505.png',
    'Juventus':             'https://media.api-sports.io/football/teams/496.png',
    'Köln':                 'https://media.api-sports.io/football/teams/162.png',
    'Lazio':                'https://media.api-sports.io/football/teams/487.png',
    'Le Havre':             'https://media.api-sports.io/football/teams/1100.png',
    'Lecce':                'https://media.api-sports.io/football/teams/867.png',
    'Leeds United':         'https://media.api-sports.io/football/teams/63.png',
    'Lens':                 'https://media.api-sports.io/football/teams/116.png',
    'Levante':              'https://media.api-sports.io/football/teams/532.png',
    'Leverkusen':           'https://media.api-sports.io/football/teams/168.png',
    'Lille':                'https://media.api-sports.io/football/teams/79.png',
    'Liverpool':            'https://media.api-sports.io/football/teams/40.png',
    'Lorient':              'https://media.api-sports.io/football/teams/111.png',
    'Lyon':                 'https://media.api-sports.io/football/teams/80.png',
    'Mainz 05':             'https://media.api-sports.io/football/teams/164.png',
    'Mallorca':             'https://media.api-sports.io/football/teams/724.png',
    'Manchester City':      'https://media.api-sports.io/football/teams/50.png',
    'Manchester Utd':       'https://media.api-sports.io/football/teams/33.png',
    'Marseille':            'https://media.api-sports.io/football/teams/81.png',
    'Metz':                 'https://media.api-sports.io/football/teams/112.png',
    'Milan':                'https://media.api-sports.io/football/teams/489.png',
    'Monaco':               'https://media.api-sports.io/football/teams/91.png',
    'Nantes':               'https://media.api-sports.io/football/teams/83.png',
    'Napoli':               'https://media.api-sports.io/football/teams/492.png',
    'Newcastle United':     'https://media.api-sports.io/football/teams/34.png',
    'Nice':                 'https://media.api-sports.io/football/teams/84.png',
    'Nottingham Forest':    'https://media.api-sports.io/football/teams/65.png',
    'Osasuna':              'https://media.api-sports.io/football/teams/727.png',
    'Oviedo':               'https://media.api-sports.io/football/teams/1008.png',
    'Paris FC':             'https://media.api-sports.io/football/teams/96.png',
    'Paris Saint-Germain':  'https://media.api-sports.io/football/teams/85.png',
    'Parma':                'https://media.api-sports.io/football/teams/509.png',
    'Pisa':                 'https://media.api-sports.io/football/teams/488.png',
    'RB Leipzig':           'https://media.api-sports.io/football/teams/173.png',
    'Rayo Vallecano':       'https://media.api-sports.io/football/teams/728.png',
    'Real Betis':           'https://media.api-sports.io/football/teams/543.png',
    'Real Madrid':          'https://media.api-sports.io/football/teams/541.png',
    'Real Sociedad':        'https://media.api-sports.io/football/teams/548.png',
    'Rennes':               'https://media.api-sports.io/football/teams/94.png',
    'Roma':                 'https://media.api-sports.io/football/teams/497.png',
    'Sassuolo':             'https://media.api-sports.io/football/teams/498.png',
    'Sevilla':              'https://media.api-sports.io/football/teams/536.png',
    'St Pauli':             'https://media.api-sports.io/football/teams/182.png',
    'Strasbourg':           'https://media.api-sports.io/football/teams/95.png',
    'Stuttgart':            'https://media.api-sports.io/football/teams/172.png',
    'Sunderland':           'https://media.api-sports.io/football/teams/71.png',
    'Torino':               'https://media.api-sports.io/football/teams/506.png',
    'Tottenham Hotspur':    'https://media.api-sports.io/football/teams/47.png',
    'Toulouse':             'https://media.api-sports.io/football/teams/97.png',
    'Udinese':              'https://media.api-sports.io/football/teams/494.png',
    'Union Berlin':         'https://media.api-sports.io/football/teams/180.png',
    'Alavés':               'https://media.api-sports.io/football/teams/542.png',
    'Angers':               'https://media.api-sports.io/football/teams/78.png',
    'Valencia':             'https://media.api-sports.io/football/teams/532.png',
    'Villarreal':           'https://media.api-sports.io/football/teams/533.png',
    'Werder Bremen':        'https://media.api-sports.io/football/teams/161.png',
    'West Ham United':      'https://media.api-sports.io/football/teams/48.png',
    'Wolfsburg':            'https://media.api-sports.io/football/teams/171.png',
    'Wolves':               'https://media.api-sports.io/football/teams/39.png',
}

# ── Helper Functions ───────────────────────────────────────────────
import pandas as pd

def get_flag_url(nation):
    if pd.isna(nation):
        return None
    nation_str = str(nation).strip()
    if not nation_str:
        return None
    parts = nation_str.split()
    if not parts:
        return None
    # Use the first token which is the 2-letter code in this dataset.
    code = parts[0].lower()
    # Handle UK home nations where flagcdn uses gb-*
    special_codes = {
        'eng': 'gb-eng',
        'sct': 'gb-sct',
        'wal': 'gb-wls',
        'nir': 'gb-nir',
    }
    flag_code = special_codes.get(code, code)
    return f"https://flagcdn.com/24x18/{flag_code}.png"

def club_logo_html(squad, size=24):
    url = CLUB_LOGOS.get(squad)
    if url:
        return f'<img src="{url}" width="{size}" height="{size}" style="vertical-align:middle; margin-right:6px;" onerror="this.style.display=\'none\'">'
    return ''

def flag_html(nation, size=18):
    url = get_flag_url(nation)
    if url:
        return (
            f'<img src="{url}" width="{size}" height="{size}" '
            f'style="vertical-align:middle; margin-right:6px;" '
            f'onerror="this.style.display=\'none\'">'
        )
    return ''

def league_logo_html(comp, size=24):
    url = LEAGUE_LOGOS.get(comp)
    if url:
        return f'<img src="{url}" width="{size}" height="{size}" style="vertical-align:middle; margin-right:6px;" onerror="this.style.display=\'none\'">'
    return ''

def normalize_stat(val, col, df):
    min_val = df[col].min()
    max_val = df[col].max()
    if max_val == min_val:
        return 0
    return float((val - min_val) / (max_val - min_val))