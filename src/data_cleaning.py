import pandas as pd
import numpy as np

print("Loading datasets...")

# Load both datasets
df_2526 = pd.read_csv('data/raw/players_data-2025_2026.csv', encoding='utf-8')
df_2425 = pd.read_excel('data/raw/top5-players24-25.xlsx')

print(f"2025-26 dataset: {df_2526.shape}")
print(f"2024-25 dataset: {df_2425.shape}")

# ── Clean 2025-26 dataset ──────────────────────────────────────────
print("\nCleaning 2025-26 dataset...")

# Keep only useful columns
cols_2526 = ['Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Min',
             'Gls', 'Ast', 'CrdY', 'CrdR', 'Sh', 'SoT', 'TklW', 'Int', 'Fls']

df_2526 = df_2526[cols_2526].copy()

# ── Clean 2024-25 dataset ──────────────────────────────────────────
print("Cleaning 2024-25 dataset...")

# Keep only advanced stat columns
cols_2425 = ['Player', 'Squad', 'xG', 'npxG', 'xAG', 'PrgC', 'PrgP', 'PrgR',
             'xG_90', 'xAG_90', 'npxG_90']

df_2425 = df_2425[cols_2425].copy()

# ── Clean player names for merging ────────────────────────────────
def clean_name(name):
    if pd.isna(name):
        return name
    return str(name).strip().lower()

df_2526['Player_clean'] = df_2526['Player'].apply(clean_name)
df_2425['Player_clean'] = df_2425['Player'].apply(clean_name)

# ── Merge datasets ─────────────────────────────────────────────────
print("\nMerging datasets...")
df = pd.merge(df_2526, df_2425, on='Player_clean', how='left', suffixes=('', '_adv'))

print(f"Merged shape: {df.shape}")
print(f"Players with xG data: {df['xG'].notna().sum()}")

# ── Basic cleaning ─────────────────────────────────────────────────
print("\nCleaning data...")

# Drop duplicate player column from merge
if 'Squad_adv' in df.columns:
    df.drop(columns=['Squad_adv'], inplace=True)

# Clean age column (remove days like "25-198" → 25)
df['Age'] = df['Age'].astype(str).str.split('-').str[0]
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

# Clean minutes
df['Min'] = pd.to_numeric(df['Min'].astype(str).str.replace(',', ''), errors='coerce')

# Filter players with less than 90 minutes
df = df[df['Min'] >= 90].copy()
print(f"After filtering low minutes: {df.shape}")

# Drop duplicates
df.drop_duplicates(subset=['Player_clean'], keep='first', inplace=True)
print(f"After dropping duplicates: {df.shape}")

# Drop helper column
df.drop(columns=['Player_clean'], inplace=True)

# Flag players with advanced stats before filling missing values
if 'xG' in df.columns:
    df['has_advanced_stats'] = df['xG'].notna()
else:
    df['has_advanced_stats'] = False

# Fill missing advanced stats with 0
adv_cols = ['xG', 'npxG', 'xAG', 'PrgC', 'PrgP', 'PrgR', 'xG_90', 'xAG_90', 'npxG_90']
for col in adv_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# ── Per 90 calculations ────────────────────────────────────────────
print("\nCalculating per 90 stats...")
df['90s'] = df['Min'] / 90

def per90(col):
    return (df[col] / df['90s']).round(2)

df['Gls_p90'] = per90('Gls')
df['Ast_p90'] = per90('Ast')
df['Sh_p90']  = per90('Sh')
df['SoT_p90'] = per90('SoT')
df['TklW_p90'] = per90('TklW')
df['Int_p90']  = per90('Int')
df['Fls_p90']  = per90('Fls')

# ── Save ───────────────────────────────────────────────────────────
df.to_csv('data/processed/cleaned_players.csv', index=False)
print(f"\n✅ Saved cleaned_players.csv")
print(f"Final shape: {df.shape}")
print(f"\nFinal columns:\n{df.columns.tolist()}")