import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==================================================
# Page setup
# ==================================================
st.set_page_config(page_title="Team Event Simulator", layout="wide")

st.title("🤺 Team Event Simulator")

# --------------------------------------------------
# Session state
# --------------------------------------------------
if "run_sim" not in st.session_state:
    st.session_state.run_sim = False

if "match_df" not in st.session_state:
    st.session_state.match_df = None

# ==================================================
# Weapon / Category selector
# ==================================================
CATEGORY_CONFIG = {
    "Women's Epee": {
        "ratings_path": "datasets/womens_epee/Women's Epee Ratings.csv",
        "rating_col": "rating_pool",
        "RD_col": "RD_pool",
    },
    "Women's Foil": {
        "ratings_path": "datasets/womens_foil/Women's Foil Ratings.csv",
        "rating_col": "rating_pool",
        "RD_col": "RD_pool",
    },
    "Women's Saber": {
        "ratings_path": "datasets/womens_saber/Women's Saber Ratings.csv",
        "rating_col": "rating_pool",
        "RD_col": "RD_pool",
    },
    "Men's Epee": {
        "ratings_path": "datasets/mens_epee/Men's Epee Ratings.csv",
        "rating_col": "rating_pool",
        "RD_col": "RD_pool",
    },
    "Men's Foil": {
        "ratings_path": "datasets/mens_foil/Men's Foil Ratings.csv",
        "rating_col": "rating_pool",
        "RD_col": "RD_pool",
    },
    "Men's Saber": {
        "ratings_path": "datasets/mens_saber/Men's Saber Ratings.csv",
        "rating_col": "rating_pool",
        "RD_col": "RD_pool",
    },
}

category = st.selectbox("Select Weapon / Category", CATEGORY_CONFIG.keys())
config = CATEGORY_CONFIG[category]

ratings = pd.read_csv(config["ratings_path"])
ratings["player"] = ratings["player"].astype(str).str.strip()

players = ratings["player"].tolist()
rating_col = config["rating_col"]
RD_col = config["RD_col"]

st.caption(f"Category selected: {category}")

# ==================================================
# Glicko helpers
# ==================================================
def scale_rating(r):
    return (r - 1500) / 173.7178

def scale_RD(rd):
    return rd / 173.7178

def g(rd):
    return 1 / np.sqrt(1 + (3 * rd**2) / (np.pi**2))

def win_prob(r1, r2, rd2):
    return 1 / (1 + np.exp(-g(rd2) * (r1 - r2)))

# ==================================================
# Team lineup selection (ROLE-BASED)
# ==================================================
st.markdown("## 🤺 Team Lineups")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Team A")
    A1 = st.selectbox("Lead-off / 3rd Man", players, key="A1")
    A2 = st.selectbox("Second", players, key="A2")
    A3 = st.selectbox("Anchor", players, key="A3")

with col2:
    st.subheader("Team B")
    B3 = st.selectbox("Lead-off / 3rd Man", players, key="B3")
    B1 = st.selectbox("Second", players, key="B1")
    B2 = st.selectbox("Anchor", players, key="B2")

teamA = [A1, A2, A3]
teamB = [B1, B2, B3]

if len(set(teamA)) < 3 or len(set(teamB)) < 3:
    st.error("Each team must have three DIFFERENT fencers.")
    st.stop()

# ==================================================
# Relay order (standard FIE)
# ==================================================
relay_order = [
    (0, 0, 5),
    (1, 1, 10),
    (2, 2, 15),
    (0, 1, 20),
    (1, 2, 25),
    (2, 0, 30),
    (0, 2, 35),
    (1, 0, 40),
    (2, 1, 45),
]

# ==================================================
# Extract stats
# ==================================================
def get_stats(name):
    row = ratings[ratings["player"] == name].iloc[0]
    return scale_rating(row[rating_col]), scale_RD(row[RD_col])

teamA_stats = [get_stats(f) for f in teamA]
teamB_stats = [get_stats(f) for f in teamB]

# ==================================================
# Simulation settings
# ==================================================
sims = st.slider("Monte Carlo simulations", 1000, 10000, 5000, 1000)

if st.button("▶️ Run Team Simulation"):
    st.session_state.run_sim = True

if not st.session_state.run_sim:
    st.warning("Run the simulation to see results.")
    st.stop()

# ==================================================
# Monte Carlo simulation
# ==================================================
results = []
score_diffs = []

for _ in range(sims):
    scoreA = scoreB = 0

    for iA, iB, target in relay_order:
        rA, _ = teamA_stats[iA]
        rB, rdB = teamB_stats[iB]

        pA = win_prob(rA, rB, rdB)
        touches = target - max(scoreA, scoreB)

        if touches <= 0:
            break

        A_hits = np.random.binomial(touches, pA)
        scoreA += A_hits
        scoreB += touches - A_hits

    results.append(scoreA > scoreB)
    score_diffs.append(scoreA - scoreB)

results = np.array(results)
score_diffs = np.array(score_diffs)

# ==================================================
# Single match simulation
# ==================================================
def simulate_single_match():
    rows = []
    scoreA = scoreB = 0

    for bout, (iA, iB, target) in enumerate(relay_order, 1):
        rA, _ = teamA_stats[iA]
        rB, rdB = teamB_stats[iB]

        pA = win_prob(rA, rB, rdB)
        touches = target - max(scoreA, scoreB)

        if touches <= 0:
            break

        A_hits = np.random.binomial(touches, pA)
        B_hits = touches - A_hits
        
        scoreA += A_hits
        scoreB += B_hits

        rows.append({
            "Bout": bout,
            "Team A": teamA[iA],
            "A Touches": A_hits,
            "Score A": scoreA,
            "Target": target,
            "Score B": scoreB,
            "B Touches": B_hits,
            "Team B": teamB[iB],
        })

    return pd.DataFrame(rows)


st.markdown("## 📋 Single Match Score Sheet")

if st.button("🎯 Simulate One Match"):
    st.session_state.match_df = simulate_single_match()

if st.session_state.match_df is not None:
    df = st.session_state.match_df
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown(
        f"""
        **Final Score:**  
        Team A {df.iloc[-1]['Score A']} – {df.iloc[-1]['Score B']} Team B
        """
    )

# ==================================================
# Results display
# ==================================================
st.markdown("## 🏆 Win Probabilities")

winA = results.mean()
st.write(f"**Team A:** {winA*100:.1f}%")
st.progress(winA)

st.write(f"**Team B:** {(1-winA)*100:.1f}%")
st.progress(1 - winA)

st.markdown("## 📊 Score Difference Distribution")

fig = px.histogram(score_diffs, nbins=30)
st.plotly_chart(fig, use_container_width=True)

st.caption(
    f"Expected margin: {score_diffs.mean():.2f} | "
    f"Most likely: {int(pd.Series(score_diffs).mode()[0])}"
)
