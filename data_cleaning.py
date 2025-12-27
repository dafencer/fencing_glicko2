#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:04:06 2025

@author: dancanlas
"""

import pandas as pd

# Pool Matches
df_pools = pd.read_csv('all_legs_pool_bouts.csv')

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
    'Leg': df_pools['Leg'],
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

df_de = pd.read_csv('all_legs_de_bouts.csv')

# Remove Bye Rounds
df_de = df_de[df_de['Score'].notna() & (df_de['Score'] != "")]

# Parse Scores
scores_de = df_de['Score'].str.split('\n').str[0]
scores_split = scores_de.str.split(' - ', expand=True).astype(int)
score1 = scores_split[0]
score2 = scores_split[1]

right_score_de = df_de.apply(
    lambda row: max(score1[row.name], score2[row.name])
                if row['Winner'] == row['Right Fencer']
                else min(score1[row.name], score2[row.name]),
    axis=1
)

left_score_de = df_de.apply(
    lambda row: max(score1[row.name], score2[row.name])
                if row['Winner'] == row['Left Fencer']
                else min(score1[row.name], score2[row.name]),
    axis=1
)

# Create Margin of Victory
# Create Outcome
# Create Scaled Outcome