import os
import sys
import importlib
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go



PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import src.config as config
importlib.reload(config)

CLUSTER_COLORS = config.CLUSTER_COLORS
CLUB_LOGOS = config.CLUB_LOGOS
LEAGUE_LOGOS = config.LEAGUE_LOGOS
club_logo_html = config.club_logo_html
flag_html = config.flag_html
league_logo_html = config.league_logo_html
normalize_stat = config.normalize_stat

# ── Page Config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="World Cup 2026 Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Theme CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Background */
    .stApp { background-color: #0a1f0a !important; }
    [data-testid="stAppViewContainer"] { background-color: #0a1f0a !important; }
    [data-testid="stMain"] { background-color: #0a1f0a !important; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0d2b0d !important;
        border-right: 2px solid #4CAF50 !important;
    }

    /* Text */
    p, li, span, div { color: #e8f5e9; }
    h1 { color: #4CAF50 !important; }
    h2 { color: #66BB6A !important; }
    h3 { color: #81C784 !important; }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #4CAF50 !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] { color: #a5d6a7 !important; }

    /* Selectbox and inputs */
    [data-baseweb="select"] > div {
        background-color: #1b3a1b !important;
        border-color: #4CAF50 !important;
        color: #e8f5e9 !important;
    }

    /* Radio */
    [data-testid="stRadio"] label { color: #a5d6a7 !important; }

    /* Slider */
    [data-testid="stSlider"] label { color: #a5d6a7 !important; }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid #4CAF50 !important;
        border-radius: 8px !important;
    }

    /* Progress bar */
    [data-testid="stProgress"] > div > div {
        background-color: #4CAF50 !important;
    }

    /* Player card */
    .player-card {
        background: linear-gradient(135deg, #0d2b0d, #1b3a1b);
        border: 1px solid #4CAF50;
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
        transition: transform 0.2s;
    }
    .player-card:hover { transform: translateY(-2px); }

    /* Stat card */
    .stat-card {
        background: linear-gradient(135deg, #0d2b0d, #1a3a1a);
        border: 1px solid #2e7d32;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 5px;
    }

    /* Divider */
    hr { border-color: #2e7d32 !important; }

    /* Sidebar title */
    .sidebar-title {
        color: #4CAF50 !important;
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
        padding: 10px 0;
    }

    /* Badge */
    .cluster-badge {
        background-color: #1b5e20;
        color: #a5d6a7;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        border: 1px solid #4CAF50;
        display: inline-block;
        margin-top: 5px;
    }

    /* Page header */
    .page-header {
        background: linear-gradient(90deg, #0d2b0d, #1b5e20);
        border-left: 4px solid #4CAF50;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv('data/processed/clustered_players.csv')

df = load_data()

# ── Sidebar ────────────────────────────────────────────────────────
st.sidebar.markdown('<div class="sidebar-title">⚽ World Cup 2026</div>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="color:#81C784; text-align:center; font-size:0.8rem;">Player Performance Analysis</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "Main Dashboard",
    "Cluster Visualization",
    "Player Comparison",
    "Similar Player Finder",
    "Insights"
])

st.sidebar.markdown("---")
st.sidebar.markdown('<p style="color:#4CAF50; font-weight:bold;">Filters</p>', unsafe_allow_html=True)

positions = df['Pos'].dropna().unique().tolist()
all_positions = ['All'] + sorted(positions)
selected_pos = st.sidebar.selectbox("Position", all_positions)

all_leagues = ['All'] + sorted(df['Comp'].dropna().unique().tolist())
selected_league = st.sidebar.selectbox("League", all_leagues)

min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))

all_clusters = ['All'] + sorted(df['Cluster_Label'].dropna().unique().tolist())
selected_cluster = st.sidebar.selectbox("Playing Style", all_clusters)

# ── Apply Filters ──────────────────────────────────────────────────
filtered_df = df.copy()
if selected_pos != 'All':
    filtered_df = filtered_df[filtered_df['Pos'].str.contains(selected_pos, na=False)]
if selected_league != 'All':
    filtered_df = filtered_df[filtered_df['Comp'] == selected_league]
if selected_cluster != 'All':
    filtered_df = filtered_df[filtered_df['Cluster_Label'] == selected_cluster]
filtered_df = filtered_df[
    (filtered_df['Age'] >= age_range[0]) &
    (filtered_df['Age'] <= age_range[1])
]

# ══════════════════════════════════════════════════════════════════
# PAGE 1 — MAIN DASHBOARD
# ══════════════════════════════════════════════════════════════════

if page == "Main Dashboard":
    st.markdown('<div class="page-header"><h1>World Cup 2026 — Player Performance Analysis</h1><p style="color:#a5d6a7;">Big 5 European Leagues · 2025/26 Season · Powered by FBref Data</p></div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Players", f"{len(filtered_df):,}")
    with col2:
        st.metric("Avg Age", f"{filtered_df['Age'].mean():.1f}")
    with col3:
        st.metric("Avg xG / 90", f"{filtered_df['xG_90'].mean():.2f}")
    with col4:
        st.metric("Playing Styles", filtered_df['Cluster_Label'].nunique())

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top Scorers (xG per 90)")
        top_scorers = filtered_df.nlargest(10, 'xG_90')[['Player', 'Squad', 'xG_90', 'Cluster_Label']]
        fig = px.bar(top_scorers, x='xG_90', y='Player', orientation='h',
                 color='Cluster_Label', template='plotly_dark',
                     color_discrete_map=CLUSTER_COLORS)
        fig.update_layout(plot_bgcolor='#0a1f0a', paper_bgcolor='#0a1f0a',
                          showlegend=False, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top Assisters (xAG per 90)")
        top_assisters = filtered_df.nlargest(10, 'xAG_90')[['Player', 'Squad', 'xAG_90', 'Cluster_Label']]
        fig2 = px.bar(top_assisters, x='xAG_90', y='Player', orientation='h',
                  color='Cluster_Label', template='plotly_dark',
                      color_discrete_map=CLUSTER_COLORS)
        fig2.update_layout(plot_bgcolor='#0a1f0a', paper_bgcolor='#0a1f0a',
                           showlegend=False, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Playing Style Distribution")
    cluster_counts = filtered_df['Cluster_Label'].value_counts().reset_index()
    cluster_counts.columns = ['Cluster', 'Count']
    fig3 = px.pie(cluster_counts, values='Count', names='Cluster',
                  template='plotly_dark', color='Cluster',
                  color_discrete_map=CLUSTER_COLORS, hole=0.4)
    fig3.update_layout(plot_bgcolor='#0a1f0a', paper_bgcolor='#0a1f0a')
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.subheader("Player Stats Table")
    display_cols = ['Player', 'Nation', 'Squad', 'Comp', 'Pos', 'Age',
                    'xG_90', 'xAG_90', 'PrgP', 'TklW_p90', 'Cluster_Label']
    table_df = filtered_df[display_cols].sort_values('xG_90', ascending=False).reset_index(drop=True)
    st.dataframe(table_df, use_container_width=True, height=400)

# ══════════════════════════════════════════════════════════════════
# PAGE 2 — CLUSTER VISUALIZATION
# ══════════════════════════════════════════════════════════════════
elif page == "Cluster Visualization":
    st.markdown('<div class="page-header"><h1>Player Cluster Visualization</h1><p style="color:#a5d6a7;">Each dot is a player — colored by playing style</p></div>', unsafe_allow_html=True)

    fig = px.scatter(
        filtered_df, x='PCA1', y='PCA2', color='Cluster_Label',
        hover_data={'Player': True, 'Squad': True, 'Pos': True,
                    'Age': True, 'xG_90': True, 'xAG_90': True,
                    'Cluster_Label': True, 'PCA1': False, 'PCA2': False},
        color_discrete_map=CLUSTER_COLORS, template='plotly_dark',
        title='Player Playing Style Clusters — Big 5 European Leagues 2025/26'
    )
    fig.update_traces(marker=dict(size=8, opacity=0.85))
    fig.update_layout(plot_bgcolor='#0a1f0a', paper_bgcolor='#0a1f0a',
                      height=600, legend_title='Playing Style',
                      xaxis_title='', yaxis_title='')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Cluster Breakdown")
    cols = st.columns(4)
    for i, (cluster, count) in enumerate(filtered_df['Cluster_Label'].value_counts().items()):
        with cols[i % 4]:
            avg_xg = filtered_df[filtered_df['Cluster_Label'] == cluster]['xG_90'].mean()
            st.markdown(f"""
            <div class="stat-card">
                <p style="color:#4CAF50; font-weight:bold; font-size:0.85rem;">{cluster}</p>
                <p style="color:white; font-size:1.5rem; font-weight:bold;">{count}</p>
                <p style="color:#a5d6a7; font-size:0.8rem;">avg xG/90: {avg_xg:.2f}</p>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE 3 — PLAYER COMPARISON
# ══════════════════════════════════════════════════════════════════
elif page == "Player Comparison":
    st.markdown('<div class="page-header"><h1>Player Comparison</h1><p style="color:#a5d6a7;">Compare two players side by side</p></div>', unsafe_allow_html=True)

    player_list = sorted(df['Player'].dropna().unique().tolist())
    col1, col2 = st.columns(2)
    with col1:
        player1 = st.selectbox("Select Player 1", player_list,
                               index=player_list.index('Lamine Yamal') if 'Lamine Yamal' in player_list else 0)
    with col2:
        player2 = st.selectbox("Select Player 2", player_list,
                               index=player_list.index('Vinicius Júnior') if 'Vinicius Júnior' in player_list else 1)

    p1 = df[df['Player'] == player1].iloc[0]
    p2 = df[df['Player'] == player2].iloc[0]

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        logo1 = club_logo_html(p1['Squad'], size=40)
        flag1 = flag_html(p1['Nation'], size=20)
        st.markdown(f"""
        <div class="player-card">
            <div style="display:flex; align-items:center; margin-bottom:10px;">
                {logo1}
                <h2 style="color:#4CAF50; margin:0;">{p1['Player']}</h2>
            </div>
            <p>{flag1} <span style="color:#a5d6a7;">{p1['Nation']}</span></p>
            <p>🏟️ <span style="color:white;">{p1['Squad']}</span> — <span style="color:#a5d6a7;">{p1['Comp']}</span></p>
            <p>📍 Position: <span style="color:white;">{p1['Pos']}</span></p>
            <p>🎂 Age: <span style="color:white;">{int(p1['Age'])}</span></p>
            <p>⏱️ Minutes: <span style="color:white;">{int(p1['Min'])}</span></p>
            <span class="cluster-badge">{p1['Cluster_Label']}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        logo2 = club_logo_html(p2['Squad'], size=40)
        flag2 = flag_html(p2['Nation'], size=20)
        st.markdown(f"""
        <div class="player-card" style="border-color:#66BB6A;">
            <div style="display:flex; align-items:center; margin-bottom:10px;">
                {logo2}
                <h2 style="color:#66BB6A; margin:0;">{p2['Player']}</h2>
            </div>
            <p>{flag2} <span style="color:#a5d6a7;">{p2['Nation']}</span></p>
            <p>🏟️ <span style="color:white;">{p2['Squad']}</span> — <span style="color:#a5d6a7;">{p2['Comp']}</span></p>
            <p>📍 Position: <span style="color:white;">{p2['Pos']}</span></p>
            <p>🎂 Age: <span style="color:white;">{int(p2['Age'])}</span></p>
            <p>⏱️ Minutes: <span style="color:white;">{int(p2['Min'])}</span></p>
            <span class="cluster-badge">{p2['Cluster_Label']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Radar Chart Comparison")

    radar_stats = ['xG_90', 'xAG_90', 'Sh_p90', 'TklW_p90', 'Int_p90', 'PrgP', 'PrgC']
    radar_labels = ['xG/90', 'xAG/90', 'Shots/90', 'Tackles/90', 'Interceptions/90', 'Prog Passes', 'Prog Carries']

    def normalize(val, col):
        min_val = df[col].min()
        max_val = df[col].max()
        if max_val == min_val:
            return 0
        return float((val - min_val) / (max_val - min_val))

    p1_values = [normalize(p1[s], s) for s in radar_stats]
    p2_values = [normalize(p2[s], s) for s in radar_stats]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=p1_values + [p1_values[0]], theta=radar_labels + [radar_labels[0]],
        fill='toself', name=player1, line_color='#4CAF50',
        fillcolor='rgba(76,175,80,0.2)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=p2_values + [p2_values[0]], theta=radar_labels + [radar_labels[0]],
        fill='toself', name=player2, line_color='#FFD700',
        fillcolor='rgba(255,215,0,0.2)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1]), bgcolor='#0d2b0d'),
        paper_bgcolor='#0a1f0a', template='plotly_dark', height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Stats Comparison Table")
    compare_df = pd.DataFrame({
        'Stat': ['xG per 90', 'xAG per 90', 'Shots per 90', 'Progressive Passes',
                 'Progressive Carries', 'Tackles Won p90', 'Interceptions p90', 'Minutes Played'],
        player1: [p1['xG_90'], p1['xAG_90'], p1['Sh_p90'], p1['PrgP'],
                  p1['PrgC'], p1['TklW_p90'], p1['Int_p90'], int(p1['Min'])],
        player2: [p2['xG_90'], p2['xAG_90'], p2['Sh_p90'], p2['PrgP'],
                  p2['PrgC'], p2['TklW_p90'], p2['Int_p90'], int(p2['Min'])]
    })
    st.dataframe(compare_df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════
# PAGE 4 — SIMILAR PLAYER FINDER
# ══════════════════════════════════════════════════════════════════
elif page == "Similar Player Finder":
    st.markdown('<div class="page-header"><h1>Similar Player Finder</h1><p style="color:#a5d6a7;">Find players with similar playing styles using cosine similarity</p></div>', unsafe_allow_html=True)

    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.preprocessing import StandardScaler

    sim_features = ['Gls_p90', 'Ast_p90', 'Sh_p90', 'SoT_p90',
                    'xG_90', 'xAG_90', 'PrgC', 'PrgP', 'TklW_p90', 'Int_p90', 'Fls_p90']

    sim_df = df.dropna(subset=sim_features).copy()
    X_sim = sim_df[sim_features].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_sim)

    player_list = sorted(sim_df['Player'].dropna().unique().tolist())
    selected_player = st.selectbox("Select a player:",
                                   player_list,
                                   index=player_list.index('Lamine Yamal') if 'Lamine Yamal' in player_list else 0)
    n_similar = st.slider("Number of similar players", 3, 15, 5)

    player_data = sim_df[sim_df['Player'] == selected_player].iloc[0]
    logo_html = club_logo_html(player_data['Squad'], size=40)
    flag = flag_html(player_data['Nation'])

    st.markdown(f"""
    <div class="player-card">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
            {logo_html}
            <h2 style="color:#4CAF50; margin:0;">{player_data['Player']}</h2>
            {flag}
        </div>
        <p>🏟️ {player_data['Squad']} — {player_data['Comp']} &nbsp;|&nbsp;
           📍 {player_data['Pos']} &nbsp;|&nbsp;
           🎂 {int(player_data['Age'])} years</p>
        <span class="cluster-badge">{player_data['Cluster_Label']}</span>
    </div>
    """, unsafe_allow_html=True)

    sim_df_reset = sim_df.reset_index(drop=True)
    player_pos = sim_df_reset[sim_df_reset['Player'] == selected_player].index[0]
    similarities = cosine_similarity([X_scaled[player_pos]], X_scaled)[0]
    sim_df_reset['Similarity'] = similarities
    similar_players = sim_df_reset[sim_df_reset['Player'] != selected_player].nlargest(n_similar, 'Similarity')

    st.markdown("---")
    st.subheader(f"Most Similar Players to {selected_player}")

    for i, (_, row) in enumerate(similar_players.iterrows()):
        sim_pct = row['Similarity'] * 100
        logo = club_logo_html(row['Squad'], size=28)
        flag = flag_html(row['Nation'])
        st.markdown(f"""
        <div class="player-card" style="padding:12px 16px;">
            <div style="display:flex; align-items:center; justify-content:space-between;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="color:#4CAF50; font-size:1.2rem; font-weight:bold;">#{i+1}</span>
                    {logo}
                    <div>
                        <p style="margin:0; font-weight:bold; color:white;">{row['Player']}</p>
                        <p style="margin:0; font-size:0.8rem; color:#a5d6a7;">{flag} {row['Squad']} · {row['Pos']} · Age {int(row['Age'])}</p>
                    </div>
                </div>
                <div style="text-align:right;">
                    <p style="color:#4CAF50; font-size:1.3rem; font-weight:bold; margin:0;">{sim_pct:.1f}%</p>
                    <span class="cluster-badge">{row['Cluster_Label']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader(f"Style Comparison — {selected_player} vs Top 3")
    radar_stats = ['xG_90', 'xAG_90', 'Sh_p90', 'TklW_p90', 'Int_p90', 'PrgP']
    radar_labels = ['xG/90', 'xAG/90', 'Shots/90', 'Tackles/90', 'Interceptions/90', 'Prog Passes']

    def normalize(val, col):
        min_val = sim_df[col].min()
        max_val = sim_df[col].max()
        if max_val == min_val:
            return 0
        return float((val - min_val) / (max_val - min_val))

    colors = ['#4CAF50', '#FFD700', '#FF6B6B', '#64B5F6']
    fig = go.Figure()
    p_vals = [normalize(player_data[s], s) for s in radar_stats]
    fig.add_trace(go.Scatterpolar(
        r=p_vals + [p_vals[0]], theta=radar_labels + [radar_labels[0]],
        fill='toself', name=selected_player,
        line_color=colors[0], fillcolor='rgba(76,175,80,0.15)'
    ))
    for i, (_, row) in enumerate(similar_players.head(3).iterrows()):
        vals = [normalize(row[s], s) for s in radar_stats]
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=radar_labels + [radar_labels[0]],
            fill='toself', name=f"{row['Player']} ({row['Similarity']*100:.0f}%)",
            line_color=colors[i+1], fillcolor='rgba(255,255,255,0.05)'
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1]), bgcolor='#0d2b0d'),
        paper_bgcolor='#0a1f0a', template='plotly_dark', height=500
    )
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# PAGE 5 — INSIGHTS
# ══════════════════════════════════════════════════════════════════
elif page == "Insights":
    st.markdown('<div class="page-header"><h1>World Cup 2026 Insights</h1><p style="color:#a5d6a7;">Data-driven discoveries from the Big 5 European Leagues</p></div>', unsafe_allow_html=True)

    st.subheader("Best Young Talents (Under 23)")
    young = df[(df['Age'] <= 23) & (df['Min'] >= 500)].copy()
    young['Talent_Score'] = (
        young['xG_90'] * 0.4 +
        young['xAG_90'] * 0.3 +
        young['PrgC'] / young['PrgC'].max() * 0.3
    )
    top_young = young.nlargest(10, 'Talent_Score')[['Player', 'Squad', 'Comp', 'Age', 'xG_90', 'xAG_90', 'Cluster_Label', 'Talent_Score']]
    fig1 = px.bar(top_young, x='Talent_Score', y='Player', orientation='h',
                  color='Cluster_Label', template='plotly_dark',
                  color_discrete_map=CLUSTER_COLORS,
                  hover_data=['Squad', 'Age', 'xG_90', 'xAG_90'])
    fig1.update_layout(plot_bgcolor='#0a1f0a', paper_bgcolor='#0a1f0a',
                       yaxis={'categoryorder': 'total ascending'}, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    st.subheader("Hidden Gems")
    underrated = df[(df['Min'] >= 200) & (df['Min'] <= 1200) & (df['xG_90'] >= 0.3)].copy()
    underrated['Value_Score'] = (
        underrated['xG_90'] * 0.5 +
        underrated['xAG_90'] * 0.3 +
        underrated['PrgP'] / underrated['PrgP'].max() * 0.2
    )
    top_underrated = underrated.nlargest(10, 'Value_Score')[['Player', 'Squad', 'Comp', 'Age', 'Min', 'xG_90', 'xAG_90', 'Cluster_Label']]
    fig2 = px.scatter(top_underrated, x='Min', y='xG_90', size='xAG_90',
                      color='Cluster_Label', hover_name='Player',
                      hover_data=['Squad', 'Age'], template='plotly_dark',
                      color_discrete_map=CLUSTER_COLORS,
                      title='High xG but Low Minutes — Hidden Gems')
    fig2.update_layout(plot_bgcolor='#0a1f0a', paper_bgcolor='#0a1f0a')
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(top_underrated.reset_index(drop=True), use_container_width=True, hide_index=True)

    st.markdown("---")

    st.subheader("Most Unique Players")
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    features = ['Gls_p90', 'Ast_p90', 'Sh_p90', 'SoT_p90', 'xG_90', 'xAG_90', 'PrgC', 'PrgP', 'TklW_p90', 'Int_p90', 'Fls_p90']
    unique_df = df.dropna(subset=features).copy()
    X = unique_df[features].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=7, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    unique_df['Uniqueness'] = kmeans.transform(X_scaled).min(axis=1)
    most_unique = unique_df.nlargest(10, 'Uniqueness')[['Player', 'Squad', 'Pos', 'Age', 'Cluster_Label', 'Uniqueness', 'xG_90', 'xAG_90', 'PrgP']]
    fig3 = px.bar(most_unique, x='Uniqueness', y='Player', orientation='h',
                  color='Cluster_Label', template='plotly_dark',
                  color_discrete_map=CLUSTER_COLORS, hover_data=['Squad', 'Age', 'xG_90'])
    fig3.update_layout(plot_bgcolor='#0a1f0a', paper_bgcolor='#0a1f0a',
                       yaxis={'categoryorder': 'total ascending'}, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    st.subheader("League Comparison")
    league_stats = df.groupby('Comp').agg(
        Avg_xG=('xG_90', 'mean'),
        Avg_xAG=('xAG_90', 'mean'),
        Players=('Player', 'count')
    ).reset_index()
    fig4 = px.bar(league_stats, x='Comp', y=['Avg_xG', 'Avg_xAG'],
                  template='plotly_dark', barmode='group',
                  color_discrete_sequence=['#4CAF50', '#FFD700'])
    fig4.update_layout(plot_bgcolor='#0a1f0a', paper_bgcolor='#0a1f0a')
    st.plotly_chart(fig4, use_container_width=True)