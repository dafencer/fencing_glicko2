#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 01:01:35 2026

@author: dancanlas
"""

import numpy as np
import pandas as pd

df = pd.read_csv("/Users/dancanlas/Projects/fencing_glicko2/Dashboard/datasets/womens_epee/cleaned_df_all_legs_we.csv")

matches = pd.DataFrame({
    'period': df['Leg'],
    'player':  df['Right Fencer'],
    'opponent':  df['Left Fencer'],
    'player_score': df['Right Score'],
    'opponent_score': df['Left Score']
})



def glicko2_ratings(matches, tau=0.5, init_rating=1500, init_RD=350, init_vol=0.06, eps=1e-6):
    """
    Compute Glicko-2 ratings from a matches DataFrame.
    
    matches: DataFrame with columns ['player', 'opponent', 'player_score', 'opponent_score', 'period']
    """
    # Constants

    # Helper functions
    def g(phi):
        return 1 / np.sqrt(1 + 3 * phi**2 / np.pi**2)
    
    def E(mu, muj, phij):
        return 1 / (1 + np.exp(-g(phij) * (mu - muj)))
    
    def f_sigma(x, delta, phi, v, a, tau):
        ex = np.exp(x)
        num = ex * (delta**2 - phi**2 - v - ex)
        den = 2 * (phi**2 + v + ex)**2
        return num / den - (x - a)/tau**2
    
    # Initialize ratings
    players = pd.unique(matches[['player', 'opponent']].values.ravel())
    ratings = pd.DataFrame({
        'player': players,
        'rating': init_rating,
        'RD': init_RD,
        'vol': init_vol
    })
    # Glicko-2 scale
    ratings['mu'] = (ratings['rating'] - 1500) / 173.7178
    ratings['phi'] = ratings['RD'] / 173.7178
    
    # Loop through periods
    for p in sorted(matches['period'].unique()):
        period_matches = matches[matches['period'] == p]
        
        for pl in pd.unique(period_matches[['player', 'opponent']].values.ravel()):
            row = ratings.loc[ratings['player'] == pl]
            mu = row['mu'].values[0]
            phi = row['phi'].values[0]
            sigma = row['vol'].values[0]
            
            # Player matches in this period
            pl_matches = period_matches[(period_matches['player'] == pl) | (period_matches['opponent'] == pl)].copy()
            if pl_matches.empty:
                # Update RD if no matches
                phi_star = np.sqrt(phi**2 + sigma**2)
                ratings.loc[ratings['player'] == pl, 'phi'] = phi_star
                continue
            
            # Compute s_j and opponent
            pl_matches['s'] = np.where(
                pl_matches['player'] == pl,
                0.5 + (pl_matches['player_score'] - pl_matches['opponent_score']) / (2 * pl_matches[['player_score', 'opponent_score']].max(axis=1)),
                0.5 + (pl_matches['opponent_score'] - pl_matches['player_score']) / (2 * pl_matches[['player_score', 'opponent_score']].max(axis=1))
            )
            pl_matches['opp'] = np.where(pl_matches['player'] == pl, pl_matches['opponent'], pl_matches['player'])
            
            mu_j = ratings.set_index('player').loc[pl_matches['opp'], 'mu'].values
            phi_j = ratings.set_index('player').loc[pl_matches['opp'], 'phi'].values
            s_j = pl_matches['s'].values
            
            # Step 3: v
            gphi = g(phi_j)
            Eij = E(mu, mu_j, phi_j)
            v = 1 / np.sum((gphi**2) * Eij * (1 - Eij))
            
            # Step 4: delta
            delta = v * np.sum(gphi * (s_j - Eij))
            
            # Step 5: volatility update
            a = np.log(sigma**2)
            if delta**2 > phi**2 + v:
                B = np.log(delta**2 - phi**2 - v)
            else:
                k = 1
                f_val = f_sigma(a - k*tau, delta, phi, v, a, tau)
                while f_val < 0:
                    k += 1
                    f_val = f_sigma(a - k*tau, delta, phi, v, a, tau)
                B = a - k*tau
            A = a
            fA = f_sigma(A, delta, phi, v, a, tau)
            fB = f_sigma(B, delta, phi, v, a, tau)
            while abs(B - A) > eps:
                C = A + (A - B) * fA / (fB - fA)
                fC = f_sigma(C, delta, phi, v, a, tau)
                if fC * fB <= 0:
                    A = B
                    fA = fB
                else:
                    fA /= 2
                B = C
                fB = fC
            sigma_prime = np.exp(A / 2)
            
            # Step 6: phi_star
            phi_star = np.sqrt(phi**2 + sigma_prime**2)
            
            # Step 7: phi_prime and mu_prime
            phi_prime = 1 / np.sqrt(1/phi_star**2 + 1/v)
            mu_prime = mu + phi_prime**2 * np.sum(gphi * (s_j - Eij))
            
            # Step 8: back to original scale
            ratings.loc[ratings['player'] == pl, ['rating', 'RD', 'vol', 'mu', 'phi']] = [
                (173.7178 * mu_prime) + init_rating, 173.7178 * phi_prime, sigma_prime, mu_prime, phi_prime
            ]
    
    return ratings[['player', 'rating', 'RD', 'vol']].sort_values('rating', ascending=False)


fencer_df = glicko2_ratings(matches)


# Filter only pool matches
df_pool = df[df['Round'].str.contains('pool', case=False, na=False)]
df_de = df[~df['Round'].str.contains('pool', case=False, na=False)]




# Pool points scored
right_points_pool = df_pool.groupby('Right Fencer')['Right Score'].sum()
left_points_pool = df_pool.groupby('Left Fencer')['Left Score'].sum()
total_points_pool = right_points_pool.add(left_points_pool, fill_value=0)

# Pool points received (opponent's points)
right_points_opponent_pool = df_pool.groupby('Right Fencer')['Left Score'].sum()
left_points_opponent_pool = df_pool.groupby('Left Fencer')['Right Score'].sum()
total_points_opponent_pool = right_points_opponent_pool.add(left_points_opponent_pool, fill_value=0)

# Count pool matches
right_count_pool = df_pool['Right Fencer'].value_counts()
left_count_pool = df_pool['Left Fencer'].value_counts()
total_count_pool = right_count_pool.add(left_count_pool, fill_value=0)

# Create fencer_df
fencer_index = total_count_pool.reset_index()
fencer_index.columns = ['player', 'Total Pool Matches']

# Align totals
scored_pool = total_points_pool.reindex(fencer_index['player']).fillna(0)
received_pool = total_points_opponent_pool.reindex(fencer_index['player']).fillna(0)
total_games_pool = total_count_pool.reindex(fencer_index['player']).fillna(0)

# Pool Touche Index
fencer_index['Pool Touche Index'] = (fencer_index['player'].map(scored_pool) - fencer_index['player'].map(received_pool))/fencer_index['player'].map(total_games_pool)


# DE points scored
right_points_de = df_de.groupby('Right Fencer')['Right Score'].sum()
left_points_de = df_de.groupby('Left Fencer')['Left Score'].sum()
total_points_de = right_points_de.add(left_points_de, fill_value=0)

# DE points received (opponent's points)
right_points_opponent_de = df_de.groupby('Right Fencer')['Left Score'].sum()
left_points_opponent_de = df_de.groupby('Left Fencer')['Right Score'].sum()
total_points_opponent_de = right_points_opponent_de.add(left_points_opponent_de, fill_value=0)

# Count de matches
right_count_de = df_de['Right Fencer'].value_counts()
left_count_de = df_de['Left Fencer'].value_counts()
total_count_de = right_count_de.add(left_count_de, fill_value=0)

# Align totals
scored_de = total_points_de.reindex(fencer_index['player']).fillna(0)
received_de = total_points_opponent_de.reindex(fencer_index['player']).fillna(0)
total_games_de = total_count_de.reindex(fencer_index['player']).fillna(0)
fencer_index['Total DE Matches'] = fencer_index['player'].map(total_games_de)
# DE Touche Index
fencer_index['DE Touche Index'] = (fencer_index['player'].map(scored_de) - fencer_index['player'].map(received_de))/fencer_index['player'].map(total_games_de)


# ---------- Pool W/L ----------
df_pool['Right Win'] = (df_pool['Right Score'] > df_pool['Left Score']).astype(int)
df_pool['Left Win'] = (df_pool['Left Score'] > df_pool['Right Score']).astype(int)

pool_wins_right = df_pool.groupby('Right Fencer')['Right Win'].sum()
pool_wins_left = df_pool.groupby('Left Fencer')['Left Win'].sum()
total_pool_wins = pool_wins_right.add(pool_wins_left, fill_value=0)
total_pool_losses = total_games_pool - total_pool_wins

fencer_index['Pool Wins'] = fencer_index['player'].map(total_pool_wins)
fencer_index['Pool Losses'] = fencer_index['player'].map(total_pool_losses)


# ---------- DE W/L ----------
df_de['Right Win'] = (df_de['Right Score'] > df_de['Left Score']).astype(int)
df_de['Left Win'] = (df_de['Left Score'] > df_de['Right Score']).astype(int)

de_wins_right = df_de.groupby('Right Fencer')['Right Win'].sum()
de_wins_left = df_de.groupby('Left Fencer')['Left Win'].sum()
total_de_wins = de_wins_right.add(de_wins_left, fill_value=0)
total_de_losses = total_games_de - total_de_wins

fencer_index['DE Wins'] = fencer_index['player'].map(total_de_wins)
fencer_index['DE Losses'] = fencer_index['player'].map(total_de_losses)


# ---------- Merge with ratings ----------
fencer_ratings_index  = pd.merge(fencer_df, fencer_index, on='player', how='outer')  # keep all fencers

fencer_ratings_index.to_csv("/Users/dancanlas/Projects/fencing_glicko2/Dashboard/datasets/womens_epee/Women's Epee Ratings.csv", index=False)
