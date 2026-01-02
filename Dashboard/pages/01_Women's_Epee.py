#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 03:13:42 2026

@author: dancanlas
"""

# -------------------------------------------------
# Fencing Head-to-Head Matchup Dashboard (Full Code)
# -------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ---------- Page Setup ----------
st.set_page_config(page_title="Women's Epee Matchup", layout="wide")
st.title("⚔️ Women's Epee Head-to-Head Matchup")


# ---------- Load Data ----------
matches_df = pd.read_csv("/Users/dancanlas/Projects/fencing_glicko2/Dashboard/datasets/womens_epee/cleaned_df_all_legs_we.csv")
fencers_df = pd.read_csv("/Users/dancanlas/Projects/fencing_glicko2/Dashboard/datasets/womens_epee/Women's Epee Ratings.csv")

# ---------- Clean Fencer Names ----------
fencers_df['player'] = fencers_df['player'].astype(str).str.strip().str.title()
players_list = fencers_df['player'].tolist()

# ---------- Fencer Selection ----------
col1, col2 = st.columns(2)

with col1:
    fencer_1 = st.selectbox("Select Fencer 1", players_list)

with col2:
    fencer_2 = st.selectbox("Select Fencer 2", players_list)

# Stop if no selection
if not fencer_1 or not fencer_2:
    st.warning("Please select both fencers.")
    st.stop()

# Stop if same fencer selected
if fencer_1 == fencer_2:
    st.warning("Please select two different fencers.")
    st.stop()


# ---------- Pull Selected Fencer Stats Safely ----------
f1_df = fencers_df[fencers_df['player'].str.strip().str.lower() == fencer_1.strip().lower()]
f2_df = fencers_df[fencers_df['player'].str.strip().str.lower() == fencer_2.strip().lower()]

if f1_df.empty or f2_df.empty:
    st.error("One of the selected fencers is not found in the ratings CSV.")
    st.stop()

f1 = f1_df.iloc[0]
f2 = f2_df.iloc[0]

rating_1 = f1['rating']
rating_2 = f2['rating']





# ---------- Glicko Based Probability ----------
prob_1 = 1 / (1 + 10 ** ((rating_2 - rating_1) / 400))
prob_2 = 1 - prob_1

favored_fencer = fencer_1 if prob_1 > prob_2 else fencer_2
favored_prob = prob_1 if prob_1 > prob_2 else prob_2
favored_color = "#1E90FF" if favored_fencer == fencer_1 else "#2ECC71"


# ---------- Head-to-Head Records ----------
head_to_head = matches_df[
    ((matches_df['Right Fencer'].str.strip().str.lower() == fencer_1.strip().lower()) &
     (matches_df['Left Fencer'].str.strip().str.lower() == fencer_2.strip().lower())) |
    ((matches_df['Right Fencer'].str.strip().str.lower() == fencer_2.strip().lower()) &
     (matches_df['Left Fencer'].str.strip().str.lower() == fencer_1.strip().lower()))
].sort_values(by="Leg", ascending=False)

if head_to_head.empty:
    wins_1 = wins_2 = total_matches = 0
    last_match_display = "No match data"
else:
    # Initialize counters
    wins_1 = wins_2 = 0

    for _, row in head_to_head.iterrows():
        # Determine which fencer is Right and which is Left
        if row['Right Fencer'].strip().lower() == fencer_1.strip().lower():
            # Right = fencer_1
            if row['Outcome'] == 1:
                wins_1 += 1
            else:
                wins_2 += 1
        else:
            # Right = fencer_2, Left = fencer_1
            if row['Outcome'] == 1:
                wins_2 += 1
            else:
                wins_1 += 1

    total_matches = head_to_head.shape[0]

    last = head_to_head.iloc[0]
    
    leg_full = int(last['Leg'])
    year = leg_full // 10
    leg_num = leg_full % 10
    
    # Determine which score belongs to fencer_1 and fencer_2
    if last['Right Fencer'].strip().lower() == fencer_1.strip().lower():
        last_match_display = (
        f"{last['Right Score']}-{last['Left Score']}  "
        f"({last['Round']}, {year} Leg {leg_num})"
        )
    else:
        last_match_display = (
            f"{last['Left Score']}-{last['Right Score']}  "
            f"({last['Round']}, {year} Leg {leg_num})"
        )


# =======================================================
#                     DISPLAY LAYOUT
# =======================================================

left, mid, right = st.columns([4, 3, 4])

# ---- Fencer 1 Panel ----
with left:
    st.markdown(
        f"""
        <h1 style="color:#1E90FF;">{fencer_1}</h1>
        Pool Touche Index: {f1['Pool Touche Index']}<br>
        DE Touche Index: {f1['DE Touche Index']}<br>
        Glicko 2 Rating: {rating_1}
        """,
        unsafe_allow_html=True
    )


# ---- Center Panel (Head to Head + Gauge) ----
with mid:
    st.markdown("### 🆚 Head-to-Head Record")
    st.write(f"**Record:** {wins_1}-{wins_2}")
    st.write(f"**Last Match:** {last_match_display}")
    st.markdown("---")
    st.markdown("### 🎯 Match Outcome Probability")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=favored_prob * 100,
        title={'text': f"Favored: {favored_fencer}"},
        number={'suffix': "%", "font": {"size": 38}},
        gauge={
            'axis': {'range':[0,100]},
            'bar': {'color': favored_color},
            'steps': [
                {'range': [0, 33], 'color': '#ffdddd'},
                {'range': [33, 66], 'color': '#fff5d6'},
                {'range': [66, 100], 'color': '#ddffdd'}
            ],
            'threshold': {
                'line': {'color': favored_color, 'width': 4},
                'thickness': 0.7,
                'value': favored_prob * 100
            }
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    st.write(f"📊 **{fencer_1}: {prob_1:.1%}**   |   **{fencer_2}: {prob_2:.1%}**")


# ---- Fencer 2 Panel ----
with right:
    st.markdown(
        f"""
        <h1 style="color:#2ECC71;">{fencer_2}</h1>
        Pool Touche Index: {f2['Pool Touche Index']}<br>
        DE Touche Index: {f2['DE Touche Index']}<br>
        Glicko 2 Rating: {rating_2}
        """,
        unsafe_allow_html=True
    )
