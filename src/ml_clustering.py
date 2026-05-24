import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

print("Loading cleaned data...")
df = pd.read_csv('data/processed/cleaned_players.csv')
print(f"Total players: {df.shape[0]}")

# ── Use only players with advanced stats ───────────────────────────
df_ml = df[df['has_advanced_stats'] == True].copy()
print(f"Players with advanced stats: {df_ml.shape[0]}")

# ── Filter out tiny samples to stabilize per-90 rates ──────────────
df_ml = df_ml[df_ml['90s'] >= 5].copy()
print(f"Players with 5+ 90s: {df_ml.shape[0]}")

# ── Derived features for better role separation ───────────────────
df_ml['Def_Action_p90'] = df_ml['TklW_p90'] + df_ml['Int_p90'] + df_ml['Fls_p90']
per90_denom = df_ml['90s'].replace(0, np.nan)
df_ml['PrgC_p90'] = df_ml['PrgC'] / per90_denom
df_ml['PrgP_p90'] = df_ml['PrgP'] / per90_denom
df_ml['PrgR_p90'] = df_ml['PrgR'] / per90_denom
df_ml['Prog_total_p90'] = df_ml['PrgP_p90'] + df_ml['PrgC_p90'] + df_ml['PrgR_p90']
df_ml['Def_over_prog'] = df_ml['Def_Action_p90'] / (df_ml['Prog_total_p90'] + 1)
df_ml['PrgP_over_PrgC'] = df_ml['PrgP_p90'] / (df_ml['PrgC_p90'] + 1)
df_ml['Carry_share'] = df_ml['PrgC_p90'] / (df_ml['Prog_total_p90'] + 1)
df_ml['is_df'] = df_ml['Pos'].str.contains('DF', na=False).astype(int)
df_ml['is_mf'] = df_ml['Pos'].str.contains('MF', na=False).astype(int)
df_ml['is_fw'] = df_ml['Pos'].str.contains('FW', na=False).astype(int)

# ── Select features for clustering ────────────────────────────────
# These stats best describe a player's STYLE not just quality
features = [
    'Gls_p90',        # scoring threat
    'npxG_90',        # non-pen xG per 90
    'Sh_p90',         # shooting volume
    'SoT_p90',        # shot accuracy
    'Ast_p90',        # creativity
    'xAG_90',         # expected assists per 90
    'PrgC_p90',       # progressive carries per 90
    'PrgP_p90',       # progressive passes per 90
    'PrgR_p90',       # progressive receptions per 90
    'TklW_p90',       # defensive work
    'Int_p90',        # interceptions
    'Fls_p90',        # pressing/aggression
    'Def_Action_p90', # combined defensive activity
    'Prog_total_p90', # total progression per 90
    'Def_over_prog',  # defensive activity relative to progression
    'PrgP_over_PrgC', # passing vs carrying balance
    'Carry_share',    # share of progression via carries
    'is_df',           # position flags
    'is_mf',
    'is_fw',
]

print(f"\nFeatures selected: {len(features)}")
print(features)

# Extract feature matrix
X = df_ml[features].copy()

# Fill any remaining nulls with 0
X = X.fillna(0)

print(f"\nFeature matrix shape: {X.shape}")
print("\nFeature stats:")
print(X.describe().round(2))

# ── Scale the features ─────────────────────────────────────────────
print("\nScaling features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("✅ Scaling done")

# ── PCA for dimensionality reduction ──────────────────────────────
print("\nApplying PCA...")
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

explained = pca.explained_variance_ratio_ * 100
print(f"PCA Component 1 explains: {explained[0]:.1f}% of variance")
print(f"PCA Component 2 explains: {explained[1]:.1f}% of variance")
print(f"Total variance explained: {sum(explained):.1f}%")

# Add PCA components to dataframe
df_ml['PCA1'] = X_pca[:, 0]
df_ml['PCA2'] = X_pca[:, 1]
print("✅ PCA done")

# ── Elbow Method ───────────────────────────────────────────────────
print("\nRunning elbow method...")
inertias = []
silhouette_scores = []
K_range = range(2, 12)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    score = silhouette_score(X_scaled, kmeans.labels_)
    silhouette_scores.append(score)
    print(f"K={k}: Inertia={kmeans.inertia_:.0f}, Silhouette={score:.3f}")

# Plot elbow curve
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(K_range, inertias, 'bo-')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(K_range, silhouette_scores, 'ro-')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score by K')
plt.grid(True)

plt.tight_layout()
plt.savefig('notebooks/elbow_curve.png', dpi=150)
plt.show()
print("✅ Elbow curve saved to notebooks/elbow_curve.png")

# ── Apply KMeans with K=7 ──────────────────────────────────────────
print("\nApplying KMeans with K=7...")
kmeans = KMeans(n_clusters=7, random_state=42, n_init=10)
df_ml['Cluster'] = kmeans.fit_predict(X_scaled)
print("✅ KMeans done")

# ── Inspect each cluster ───────────────────────────────────────────
print("\nCluster sizes:")
print(df_ml['Cluster'].value_counts().sort_index())

print("\nCluster profiles (mean stats):")
cluster_profile = df_ml.groupby('Cluster')[features].mean().round(2)
print(cluster_profile)

# Mean stats used for label rules
cluster_means = df_ml.groupby('Cluster')[
    [
        'Gls_p90',
        'npxG_90',
        'Sh_p90',
        'PrgP_p90',
        'PrgC_p90',
        'PrgR_p90',
        'xAG_90',
        'Ast_p90',
        'TklW_p90',
        'Int_p90',
        'Fls_p90',
        'Def_Action_p90',
        'Prog_total_p90',
        'is_df',
        'is_mf',
        'is_fw',
        'Def_over_prog',
        'PrgP_over_PrgC',
        'Carry_share',
    ]
].mean().round(2)
cluster_means = cluster_means.loc[~cluster_means.index.duplicated(keep='first')]

def score_sum(columns):
    arrays = []
    for col in columns:
        series = cluster_means[col]
        if isinstance(series, pd.DataFrame):
            series = series.iloc[:, 0]
        arrays.append(series.to_numpy(dtype=float).reshape(1, -1))
    values = np.sum(np.vstack(arrays), axis=0)
    return pd.Series(values, index=cluster_means.index)
print("\nCluster means (label features):")
print(cluster_means)

print("\nSample players per cluster:")
for i in range(7):
    print(f"\n--- Cluster {i} ---")
    cluster_players = df_ml[df_ml['Cluster'] == i][['Player', 'Squad', 'Pos', 'Min', 'npxG_90', 'xAG_90', 'TklW_p90', 'Int_p90', 'PrgP_p90']].head(8)
    print(cluster_players.to_string())

# ── Assign cluster labels based on mean stats ─────────────────────
def pick_best(series, remaining, highest=True, mask=None):
    candidates = series.loc[list(remaining)]
    if mask is not None:
        mask = mask.loc[candidates.index]
        candidates = candidates[mask]
    if candidates.empty:
        candidates = series.loc[list(remaining)]
    return candidates.idxmax() if highest else candidates.idxmin()

remaining = set(cluster_profile.index.tolist())
cluster_labels = {}

fw_mask = cluster_means['is_fw'] >= 0.4
mf_mask = cluster_means['is_mf'] >= 0.6
df_mask = cluster_means['is_df'] >= 0.4
cb_mask = cluster_means['is_df'] >= 0.7
gk_mask = (cluster_means['is_df'] + cluster_means['is_mf'] + cluster_means['is_fw']) <= 0.1

# Goalkeepers: very low outfield position flags and attacking output
if gk_mask.any():
    goalkeepers = pick_best(
        score_sum(['npxG_90', 'Sh_p90']) + (cluster_means['is_df'] + cluster_means['is_mf'] + cluster_means['is_fw']),
        remaining,
        highest=False,
        mask=gk_mask
    )
    cluster_labels[goalkeepers] = 'Goalkeepers'
    remaining.remove(goalkeepers)

# Pure Strikers: highest npxG_90 + Sh_p90 + Gls_p90
pure_strikers = pick_best(
    score_sum(['npxG_90', 'Sh_p90', 'Gls_p90']),
    remaining,
    highest=True,
    mask=fw_mask
)
cluster_labels[pure_strikers] = 'Pure Strikers'
remaining.remove(pure_strikers)

# Wide Attackers: high carry share and progressive runs
wide_attackers = pick_best(
    score_sum(['Carry_share', 'PrgC_p90', 'PrgR_p90', 'npxG_90']),
    remaining,
    highest=True,
    mask=fw_mask
)
cluster_labels[wide_attackers] = 'Wide Attackers'
remaining.remove(wide_attackers)

# Progressive Fullbacks: high progression, low goal threat
progressive_fullbacks = pick_best(
    score_sum(['Prog_total_p90']) + (0.5 * cluster_means['PrgP_p90']) +
    (0.5 * cluster_means['Def_Action_p90']) -
    (2.0 * cluster_means['npxG_90']) - (0.3 * cluster_means['Carry_share']),
    remaining,
    highest=True,
    mask=df_mask
)
cluster_labels[progressive_fullbacks] = 'Progressive Fullbacks'
remaining.remove(progressive_fullbacks)

# Creative Playmakers: high xAG/Ast with pass-dominant progression
creative_playmakers = pick_best(
    score_sum(['xAG_90', 'Ast_p90']) +
    (0.5 * cluster_means['PrgP_over_PrgC']) - (0.3 * cluster_means['Carry_share']),
    remaining,
    highest=True,
    mask=mf_mask
)
cluster_labels[creative_playmakers] = 'Creative Playmakers'
remaining.remove(creative_playmakers)

# Defensive Midfielders: strong defensive activity with passing balance
dm_score = (
    score_sum(['Def_Action_p90', 'Int_p90']) +
    (0.6 * cluster_means['PrgP_over_PrgC'])
)
defensive_mids = pick_best(dm_score, remaining, highest=True, mask=mf_mask)
cluster_labels[defensive_mids] = 'Defensive Midfielders & Destroyers'
remaining.remove(defensive_mids)

# Centre-Backs: high defense relative to progression, low goal threat
cb_score = (
    cluster_means['Def_over_prog'] -
    (0.3 * cluster_means['Prog_total_p90']) -
    (0.6 * cluster_means['npxG_90'])
)
centre_backs = pick_best(cb_score, remaining, highest=True, mask=cb_mask)
cluster_labels[centre_backs] = 'Centre-Backs & Defenders'
remaining.remove(centre_backs)

# Assign any other defender-heavy clusters to Centre-Backs
extra_cb_clusters = [c for c in list(remaining) if cluster_means.loc[c, 'is_df'] >= 0.7]
for c in extra_cb_clusters:
    cluster_labels[c] = 'Centre-Backs & Defenders'
    remaining.remove(c)

# Box-to-Box: remaining cluster
if len(remaining) == 1:
    box_to_box = remaining.pop()
    cluster_labels[box_to_box] = 'Box-to-Box Forwards'
else:
    # Fallback: assign any remaining to Box-to-Box
    for cluster_id in remaining:
        cluster_labels[cluster_id] = 'Box-to-Box Forwards'

print("\nCluster label mapping (derived):")
for k in sorted(cluster_labels.keys()):
    print(f"Cluster {k}: {cluster_labels[k]}")

df_ml['Cluster_Label'] = df_ml['Cluster'].map(cluster_labels)

# Positional overrides for edge cases
df_ml.loc[
    (df_ml['Cluster_Label'] == 'Centre-Backs & Defenders') &
    df_ml['Pos'].str.contains('MF', na=False) &
    ~df_ml['Pos'].str.contains('DF', na=False) &
    (df_ml['Def_Action_p90'] >= 2.5),
    'Cluster_Label'
] = 'Defensive Midfielders & Destroyers'

df_ml.loc[
    (df_ml['Cluster_Label'] == 'Progressive Fullbacks') &
    ~df_ml['Pos'].str.contains('DF', na=False) &
    df_ml['Pos'].str.contains('MF', na=False),
    'Cluster_Label'
] = 'Box-to-Box Forwards'

# ── Save clustered data ────────────────────────────────────────────
df_ml.to_csv('data/processed/clustered_players.csv', index=False)

print("\n✅ Saved clustered_players.csv")
print(f"Total players: {df_ml.shape[0]}")
print("\nCluster distribution:")
print(df_ml['Cluster_Label'].value_counts())

# ── Quick visualization to verify ─────────────────────────────────
import matplotlib.pyplot as plt

colors = {
    'Goalkeepers': '#90A4AE',
    'Defensive Midfielders & Destroyers': '#e74c3c',
    'Pure Strikers': '#e67e22',
    'Wide Attackers': '#f1c40f',
    'Centre-Backs & Defenders': '#2ecc71',
    'Progressive Fullbacks': '#1abc9c',
    'Creative Playmakers': '#9b59b6',
    'Box-to-Box Forwards': '#3498db'
}

plt.figure(figsize=(12, 8))
plt.style.use('dark_background')

for label, group in df_ml.groupby('Cluster_Label'):
    plt.scatter(
        group['PCA1'],
        group['PCA2'],
        c=colors[label],
        label=label,
        alpha=0.6,
        s=30
    )

plt.title('Player Clusters — World Cup 2026 Dashboard', fontsize=14)
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(loc='upper right', fontsize=8)
plt.tight_layout()
plt.savefig('notebooks/cluster_visualization.png', dpi=150)
plt.show()
print("✅ Cluster visualization saved!")