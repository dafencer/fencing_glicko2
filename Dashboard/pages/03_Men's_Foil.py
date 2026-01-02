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
st.set_page_config(page_title="Men's Foil Matchup", layout="wide")
st.title("⚔️ Men's Foil Head-to-Head Matchup")


# ---------- Load Data ----------
matches_df = pd.read_csv("/Users/dancanlas/Projects/fencing_glicko2/Dashboard/datasets/mens_foil/cleaned_df_all_legs_mf.csv")
fencers_df = pd.read_csv("/Users/dancanlas/Projects/fencing_glicko2/Dashboard/datasets/mens_foil/Men's Foil Ratings.csv")

# ---------- Clean Fencer Names ----------
fencers_df['player'] = fencers_df['player'].astype(str).str.strip()
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


# ---------- Pull Selected Fencer Stats ----------
f1_df = fencers_df[fencers_df['player'].str.strip() == fencer_1.strip()]
f2_df = fencers_df[fencers_df['player'].str.strip() == fencer_2.strip()]

if f1_df.empty or f2_df.empty:
    st.error("One of the selected fencers is not found in the ratings CSV.")
    st.stop()

f1 = f1_df.iloc[0]
f2 = f2_df.iloc[0]

rating_1 = f1['rating']
rating_2 = f2['rating']

RD_1 = f1['RD']
RD_2 = f2['RD']

# ---------- Glicko-2 Scaled ----------
def scale_rating(rating):
    return (rating - 1500) / 173.7178

def scale_RD(RD):
    return RD / 173.7178

r1 = scale_rating(rating_1)
r2 = scale_rating(rating_2)

RD1 = scale_RD(RD_1)
RD2 = scale_RD(RD_2)

def g(RD):
    return 1 / np.sqrt(1 + (3 * RD**2) / (np.pi**2))

def E(r1, r2, RD2):
    return 1 / (1 + np.exp(-g(RD2) * (r1 - r2)))

prob_1 = E(r1, r2, RD2)
prob_2 = 1 - prob_1

favored_fencer = fencer_1 if prob_1 > prob_2 else fencer_2
favored_prob = prob_1 if prob_1 > prob_2 else prob_2
favored_color = "#1E90FF" if favored_fencer == fencer_1 else "#2ECC71"


# ---------- Head-to-Head Records ----------
head_to_head = matches_df[
    ((matches_df['Right Fencer'].str.strip() == fencer_1.strip()) &
     (matches_df['Left Fencer'].str.strip() == fencer_2.strip())) |
    ((matches_df['Right Fencer'].str.strip() == fencer_2.strip()) &
     (matches_df['Left Fencer'].str.strip() == fencer_1.strip()))
].sort_values(by="Leg", ascending=False)

if head_to_head.empty:
    wins_1 = wins_2 = total_matches = 0
    last_match_display = "No match data"
else:
    wins_1 = wins_2 = 0

    for _, row in head_to_head.iterrows():
        if row['Right Fencer'].strip() == fencer_1.strip():
            if row['Outcome'] == 1:
                wins_1 += 1
            else:
                wins_2 += 1
        else:
            if row['Outcome'] == 1:
                wins_2 += 1
            else:
                wins_1 += 1

    total_matches = head_to_head.shape[0]

    last = head_to_head.iloc[0]
    leg_full = int(last['Leg'])
    year = leg_full // 10
    leg_num = leg_full % 10

    left_score = int(last['Left Score'])
    right_score = int(last['Right Score'])

    if last['Right Fencer'].strip() == fencer_1.strip():
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
        <div style="text-align:center;">
            <h2 style="color:#1E90FF; font-size:28px; margin-bottom:5px;">{fencer_1}</h2>
            <div style="line-height:1.5;">
                <b>Pool Touche Index:</b> {f1['Pool Touche Index']:.2f}<br>
                <b>DE Touche Index:</b> {f1['DE Touche Index']:.2f}<br>
                <b>Pool Record:</b> {int(f1['Pool Wins'])}-{int(f1['Pool Losses'])}<br>
                <b>DE Record:</b> {int(f1['DE Wins'])}-{int(f1['DE Losses'])}<br><br>
                <b>Glicko-2 Rating:</b> {rating_1:.2f}<br>
                <b>Rating Deviation (RD):</b> {RD_1:.2f} 
                <span style="color:gray; font-size:0.9em; font-weight:bold;">ⓘ</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("ⓘ Info"):
        st.write("Higher RD means more uncertainty in the rating estimate.")


# ---- Center Panel (Head to Head + Gauge) ----
with mid:
    # Head-to-Head Record with larger font
    st.markdown(
        "<div style='text-align:center; font-size:32px; font-weight:bold;'>🆚 Head-to-Head Record</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='text-align:center; font-size:18px; margin-top:5px;'><b>Record:</b> {wins_1}-{wins_2}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='text-align:center; font-size:16px; margin-bottom:10px;'><b>Last Match:</b> {last_match_display}</div>",
        unsafe_allow_html=True
    )

    # Divider
    st.markdown("<hr style='margin-top:5px; margin-bottom:5px;'>", unsafe_allow_html=True)

    # Match Outcome Probability heading, closer to the gauge
    st.markdown(
        "<div style='text-align:center; font-size:28px; font-weight:bold; margin-bottom:5px;'>🎯 Match Outcome Probability</div>",
        unsafe_allow_html=True
    )

    # Gauge
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

    # Probabilities below the gauge, centered
    st.markdown(
        f"<div style='text-align:center; font-size:18px; margin-top:-10px;'><b>{fencer_1}:</b> {prob_1:.1%}  |  <b>{fencer_2}:</b> {prob_2:.1%}</div>",
        unsafe_allow_html=True
    )



# ---- Fencer 2 Panel ----
with right:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <h2 style="color:#2ECC71; font-size:28px; margin-bottom:5px;">{fencer_2}</h2>
            <div style="line-height:1.5;">
                <b>Pool Touche Index:</b> {f2['Pool Touche Index']:.2f}<br>
                <b>DE Touche Index:</b> {f2['DE Touche Index']:.2f}<br>
                <b>Pool Record:</b> {int(f2['Pool Wins'])}-{int(f2['Pool Losses'])}<br>
                <b>DE Record:</b> {int(f2['DE Wins'])}-{int(f2['DE Losses'])}<br><br>
                <b>Glicko-2 Rating:</b> {rating_2:.2f}<br>
                <b>Rating Deviation (RD):</b> {RD_2:.2f} 
                <span style="color:gray; font-size:0.9em; font-weight:bold;">ⓘ</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("ⓘ Info"):
        st.write("Higher RD means more uncertainty in the rating estimate.")
