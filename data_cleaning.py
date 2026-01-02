#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:04:06 2025

@author: dancanlas
"""

import pandas as pd

# Pool Matches
df_pools = pd.read_csv("/Users/dancanlas/Projects/fencing_glicko2/Women's Epee datasets/all_legs_pool_bouts_we.csv")

# Parse Scores
right_score_pool = df_pools['Score1'].apply(lambda x: int(x.replace('V','').replace('D','')))
left_score_pool = df_pools['Score2'].apply(lambda x: int(x.replace('V','').replace('D','')))

# Create Margin of Victory
mov_pool = right_score_pool - left_score_pool

# Create outcome (1 if right fencer wins 0 if left fencer wins)
outcome_pool = (mov_pool > 0).astype(int)
# Create scaled outcome (>0.5 if right fencer wins <0.5 if left fencer wins, the closer to 1 or 0, the greater the margin of victory is)
scaled_outcome_pool = 0.5 + (mov_pool / (2 * pd.concat([right_score_pool, left_score_pool], axis=1).max(axis=1)))


cleaned_df_pools = pd.DataFrame({
    'Leg': 2025 *10 + df_pools['Leg'],
    'Round': df_pools['Pool'],
    'Right Fencer': df_pools['Right Fencer'],
    'Left Fencer': df_pools['Left Fencer'],
    'Right Score': right_score_pool,
    'Left Score': left_score_pool,
    'MOV': mov_pool,
    'Outcome': outcome_pool,
    'Scaled Outcome': scaled_outcome_pool
})

#DE Matches

df_de = pd.read_csv("/Users/dancanlas/Projects/fencing_glicko2/Women's Epee datasets/all_legs_de_bouts_we.csv")

# Remove Bye Rounds
df_de = df_de[df_de['Score'].notna() & (df_de['Score'] != "")]

# ---- FIXED SCORE PARSING ----
scores_de = df_de['Score'].astype(str).str.strip()
scores_de = scores_de.str.replace(r'[–—−]', '-', regex=True)  # normalize dash types
scores_de = scores_de.str.split('\n').str[0]                  # first line only

# extract scores like "15 - 12" or "15-12"
scores_split = scores_de.str.extract(r'(\d+)\s*-\s*(\d+)')
score1_de = pd.to_numeric(scores_split[0], errors='coerce')
score2_de = pd.to_numeric(scores_split[1], errors='coerce')

# remove rows where parsing failed
valid_mask = score1_de.notna() & score2_de.notna()
df_de = df_de[valid_mask].reset_index(drop=True)
score1_de = score1_de[valid_mask].reset_index(drop=True)
score2_de = score2_de[valid_mask].reset_index(drop=True)



right_score_de = df_de.apply(
    lambda row: max(score1_de[row.name], score2_de[row.name])
                if row['Winner'] == row['Right Fencer']
                else min(score1_de[row.name], score2_de[row.name]),
    axis=1
)

left_score_de = df_de.apply(
    lambda row: max(score1_de[row.name], score2_de[row.name])
                if row['Winner'] == row['Left Fencer']
                else min(score1_de[row.name], score2_de[row.name]),
    axis=1
)

# Create Margin of Victory
mov_de = right_score_de - left_score_de

# Create Outcome
outcome_de = (mov_de > 0).astype(int)

# Create Scaled Outcome
scaled_outcome_de = 0.5 + (mov_de / (2 * pd.concat([right_score_de, left_score_de], axis=1).max(axis=1)))

cleaned_df_de = pd.DataFrame({
    'Leg': 2025 *10 + df_de['Leg'],
    'Round': df_de['Round'],
    'Right Fencer': df_de['Right Fencer'],
    'Left Fencer': df_de['Left Fencer'],
    'Right Score': right_score_de,
    'Left Score': left_score_de,
    'MOV': mov_de,
    'Outcome': outcome_de,
    'Scaled Outcome': scaled_outcome_de
})


# append pools and de
cleaned_df_all_legs = pd.concat([cleaned_df_pools, cleaned_df_de], ignore_index=True)
print(cleaned_df_all_legs)


# Save to csv
cleaned_df_all_legs.to_csv("Women's Epee datasets/cleaned_df_all_legs_we.csv", index=False)














