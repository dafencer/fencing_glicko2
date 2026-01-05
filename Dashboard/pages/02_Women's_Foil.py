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
st.set_page_config(page_title="Women's Foil Matchup", layout="wide")



st.markdown(
    """
    <div style="position: absolute; top: 0px; left: 0px; z-index: 100;">
        <a href="/" target="_self"
           style="
               background-color:#A9A9A9;  
               color:white;
               padding:6px 12px;
               border-radius:5px;
               text-decoration:none;
               font-weight:bold;
               font-size:14px;
               display:flex;
               align-items:center;
               gap:5px;">
           &#8592; Back
        </a>
    </div>
    """,
    unsafe_allow_html=True
)



st.title("⚔️ Women's Foil Head-to-Head Matchup")


# ---------- Footer ----------
from utils import render_footer
render_footer()




# ---------- Load Data ----------
matches_df = pd.read_csv("datasets/womens_foil/cleaned_df_all_legs_wf.csv")
fencers_df = pd.read_csv("datasets/womens_foil/Women's Foil Ratings.csv")

cols = ['Pool Wins', 'Pool Losses', 'DE Wins', 'DE Losses']
fencers_df[cols] = fencers_df[cols].fillna(0).astype(int)


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

#Pool Ratings
rating_pool_1 = f1['rating_pool']
rating_pool_2 = f2['rating_pool']

RD_pool_1 = f1['RD_pool']
RD_pool_2 = f2['RD_pool']
#DE Ratings
rating_de_1 = f1['rating_de']
rating_de_2 = f2['rating_de']

RD_de_1 = f1['RD_de']
RD_de_2 = f2['RD_de']


# ---------- Glicko-2 Scaled ----------
def scale_rating(rating):
    return (rating - 1500) / 173.7178

def scale_RD(RD):
    return RD / 173.7178


#Pool
r_pool_1 = scale_rating(rating_pool_1)
r_pool_2 = scale_rating(rating_pool_2)

RD_pool1 = scale_RD(RD_pool_1)
RD_pool2 = scale_RD(RD_pool_2)

def g(RD):
    return 1 / np.sqrt(1 + (3 * RD**2) / (np.pi**2))

def E(r1, r2, RD2):
    return 1 / (1 + np.exp(-g(RD2) * (r1 - r2)))

prob_pool_1 = E(r_pool_1, r_pool_2, RD_pool2)
prob_pool_2 = 1 - prob_pool_1

favored_fencer_pool = fencer_1 if prob_pool_1 > prob_pool_2 else fencer_2
favored_prob_pool = prob_pool_1 if prob_pool_1 > prob_pool_2 else prob_pool_2
favored_color_pool = "#1E90FF" if favored_fencer_pool == fencer_1 else "#2ECC71"


#DE
r_de_1 = scale_rating(rating_de_1)
r_de_2 = scale_rating(rating_de_2)

RD_de1 = scale_RD(RD_de_1)
RD_de2 = scale_RD(RD_de_2)


prob_de_1 = E(r_de_1, r_de_2, RD_de2)
prob_de_2 = 1 - prob_de_1

favored_fencer_de = fencer_1 if prob_de_1 > prob_de_2 else fencer_2
favored_prob_de = prob_de_1 if prob_de_1 > prob_de_2 else prob_de_2
favored_color_de = "#1E90FF" if favored_fencer_de == fencer_1 else "#2ECC71"



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





rating_display_pool_1 = f"{rating_pool_1:.2f}" if rating_pool_1 == rating_pool_1 else "—"
rd_display_pool_1 = f"{RD_pool_1:.2f}" if RD_pool_1 == RD_pool_1 else "—"

rating_display_de_1 = f"{rating_de_1:.2f}" if rating_de_1 == rating_de_1 else "—"
rd_display_de_1 = f"{RD_de_1:.2f}" if RD_de_1 == RD_de_1 else "—"


rating_display_pool_2 = f"{rating_pool_2:.2f}" if rating_pool_2 == rating_pool_2 else "—"
rd_display_pool_2 = f"{RD_pool_2:.2f}" if RD_pool_2 == RD_pool_2 else "—"

rating_display_de_2 = f"{rating_de_2:.2f}" if rating_de_2 == rating_de_2 else "—"
rd_display_de_2 = f"{RD_de_2:.2f}" if RD_de_2 == RD_de_2 else "—"



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
                <b>Pool Glicko-2 Rating:</b>
                <span style="color:#CD7F32; font-weight:bold;">{rating_display_pool_1}</span>
                 | 
                <span style="color:gray;">RD: {rd_display_pool_1}</span><br>
                <b>DE Glicko-2 Rating:</b>
                <span style="color:gold; font-weight:bold;">{rating_display_de_1}</span>
                 | 
                <span style="color:gray;">RD: {rd_display_de_1}</span><br>
                <span style="color:gray; font-size:0.8em;">* Higher RD means more uncertainty in the rating estimate.</span><br>
                """, unsafe_allow_html=True)
    
  




# ---- Center Panel --------
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

    
    


# ---------- Combined Horizontal Bars for Pool & DE ----------

bars_data = [
    {"label": "Pool Match", "values": [prob_pool_1*100, prob_pool_2*100]},
    {"label": "DE Match", "values": [prob_de_1*100, prob_de_2*100]}
]


base_colors = [("#104E8B", "#1F7A50")] * 2  
highlight_colors = ["#1E90FF", "#2ECC71"] 

fig = go.Figure()

# Track legend so we only show each fencer once
legend_added = {fencer_1: False, fencer_2: False}

for i, bar in enumerate(bars_data):
    # Determine which fencer has higher probability
    if bar["values"][0] > bar["values"][1]:
        colors = [highlight_colors[0], base_colors[i][1]]  # Fencer1 highlighted
        text_colors = ["white", "#A9A9A9"]
    else:
        colors = [base_colors[i][0], highlight_colors[1]]  # Fencer2 highlighted
        text_colors = ["#A9A9A9", "white"]

    # Fencer 1
    fig.add_trace(go.Bar(
        y=[bar["label"]],
        x=[bar["values"][0]],
        name=fencer_1 if not legend_added[fencer_1] else None,  # only first trace shows name
        showlegend=not legend_added[fencer_1],                 # hide legend for subsequent traces
        orientation='h',
        marker=dict(color=colors[0]),
        text=f"{bar['values'][0]:.1f}%",
        textposition='inside',
        textfont=dict(color=text_colors[0], size=14),
        hovertemplate=f"{fencer_1}: {bar['values'][0]:.1f}%<extra></extra>"
    ))
    legend_added[fencer_1] = True

    # Fencer 2
    fig.add_trace(go.Bar(
        y=[bar["label"]],
        x=[bar["values"][1]],
        name=fencer_2 if not legend_added[fencer_2] else None,  # only first trace shows name
        showlegend=not legend_added[fencer_2],                 # hide legend for subsequent traces
        orientation='h',
        marker=dict(color=colors[1]),
        text=f"{bar['values'][1]:.1f}%",
        textposition='inside',
        textfont=dict(color=text_colors[1], size=14),
        hovertemplate=f"{fencer_2}: {bar['values'][1]:.1f}%<extra></extra>"
    ))
    legend_added[fencer_2] = True


# Layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text="🎯 Match Outcome Probabilities",
        x=0.5,
        xanchor='center',
        font=dict(size=26, color="white")
    ),
    xaxis=dict(title="", range=[0,100], showgrid=False, showticklabels=False),
    yaxis=dict(autorange="reversed", showticklabels=True, tickfont=dict(size=14)),
    height=160,
    margin=dict(l=50, r=50, t=60, b=40),
    bargap=0.25,
    barcornerradius=10,
    uniformtext_minsize=12,
    uniformtext_mode='hide'
)

st.plotly_chart(fig, use_container_width=True)
st.markdown(
    "<div style='text-align:center; font-size:13px; color:gray;'>"
    "* These probabilities reflect the predicted likelihood and margin of victory for each match."
    "</div>",
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
                <b>Pool Glicko-2 Rating:</b>
                <span style="color:#CD7F32; font-weight:bold;">{rating_display_pool_2}</span>
                 | 
                <span style="color:gray;">RD: {rd_display_pool_2}</span><br>
                <b>DE Glicko-2 Rating:</b>
                <span style="color:gold; font-weight:bold;">{rating_display_de_2}</span>
                 | 
                <span style="color:gray;">RD: {rd_display_de_2}</span><br>
                <span style="color:gray; font-size:0.8em;">* Higher RD means more uncertainty in the rating estimate.</span><br>
                """, unsafe_allow_html=True)
    
    
