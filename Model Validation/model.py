

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error


# %% Loading All weapons datasets

# Women's Epee
df_we = pd.read_csv("cleaned_df_all_legs_we.csv")
# Men's Epee
df_me = pd.read_csv("cleaned_df_all_legs_me.csv")
# Women's Foil
df_wf = pd.read_csv("cleaned_df_all_legs_wf.csv")
# Men's Foil
df_mf = pd.read_csv("cleaned_df_all_legs_mf.csv")
# Women's Saber
df_ws = pd.read_csv("cleaned_df_all_legs_ws.csv")
# Men's Saber
df_ms = pd.read_csv("cleaned_df_all_legs_ms.csv")

# %% Matches function
def prepare_matches(df, r):
    if r == 'pool':
        df_r = df[df['Round'].str.contains('pool', case=False, na=False)]
    elif r == 'de':
        df_r = df[~df['Round'].str.contains('pool', case=False, na=False)]
    else:
        raise ValueError("r must be 'pool' or 'de'")

    matches = pd.DataFrame({
        'period': df_r['Leg'],
        'player': df_r['Right Fencer'],
        'opponent': df_r['Left Fencer'],
        'player_score': df_r['Right Score'],
        'opponent_score': df_r['Left Score'],
        'outcome': df_r['Outcome'],
        'round': df_r['Round'],
        'scaled_outcome': df_r["Scaled Outcome"]
    })

    return matches

# %% Matches datasets
# Women's Epee
matches_we_pool = prepare_matches(df_we, 'pool')
matches_we_de = prepare_matches(df_we, 'de')

# Men's Epee
matches_me_pool = prepare_matches(df_me, 'pool')
matches_me_de = prepare_matches(df_me, 'de')

# Women's Foil
matches_wf_pool = prepare_matches(df_wf, 'pool')
matches_wf_de = prepare_matches(df_wf, 'de')

# Men's Foil
matches_mf_pool = prepare_matches(df_mf, 'pool')
matches_mf_de = prepare_matches(df_mf, 'de')

# Women's Saber
matches_ws_pool = prepare_matches(df_ws, 'pool')
matches_ws_de = prepare_matches(df_ws, 'de')

# Men's Saber
matches_ms_pool = prepare_matches(df_ms, 'pool')
matches_ms_de = prepare_matches(df_ms, 'de')


# %% Train-Test function (Train: Legs 1-3, Test: Legs 4-5)

def train_test(matches, t):
    if t == 'train':
        matches_t = matches[matches['period'].isin([20251, 20252, 20253])]
    elif t == 'test':
        matches_t = matches[matches['period'].isin([20254, 20255])]
    else:
        raise ValueError("t must be 'train' or 'test'")
    return matches_t

# %% Train-Test datasets

# Women's Epee
matches_we_pool_train = train_test(matches_we_pool, 'train')  # pool train
matches_we_pool_test = train_test(matches_we_pool, 'test')  # pool test

matches_we_de_train = train_test(matches_we_de, 'train')  # de train
matches_we_de_test = train_test(matches_we_de, 'test')  # de test


# Men's Epee
matches_me_pool_train = train_test(matches_me_pool, 'train')  # pool train
matches_me_pool_test = train_test(matches_me_pool, 'test')  # pool test

matches_me_de_train = train_test(matches_me_de, 'train')  # de train
matches_me_de_test = train_test(matches_me_de, 'test')  # de test

# Women's Foil
matches_wf_pool_train = train_test(matches_wf_pool, 'train')  # pool train
matches_wf_pool_test = train_test(matches_wf_pool, 'test')  # pool test

matches_wf_de_train = train_test(matches_wf_de, 'train')  # de train
matches_wf_de_test = train_test(matches_wf_de, 'test')  # de test

# Men's Foil
matches_mf_pool_train = train_test(matches_mf_pool, 'train')  # pool train
matches_mf_pool_test = train_test(matches_mf_pool, 'test')  # pool test

matches_mf_de_train = train_test(matches_mf_de, 'train')  # de train
matches_mf_de_test = train_test(matches_mf_de, 'test')  # de test

# Women's Saber
matches_ws_pool_train = train_test(matches_ws_pool, 'train')  # pool train
matches_ws_pool_test = train_test(matches_ws_pool, 'test')  # pool test

matches_ws_de_train = train_test(matches_ws_de, 'train')  # de train
matches_ws_de_test = train_test(matches_ws_de, 'test')  # de test

# Men's Saber
matches_ms_pool_train = train_test(matches_ms_pool, 'train')  # pool train
matches_ms_pool_test = train_test(matches_ms_pool, 'test')  # pool test

matches_ms_de_train = train_test(matches_ms_de, 'train')  # de train
matches_ms_de_test = train_test(matches_ms_de, 'test')  # de test

# %% Glicko 2 Function

def glicko2_ratings(matches, model_type,  tau=0.5, init_rating=1500, init_RD=350, init_vol=0.06, eps=1e-6):
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
            if model_type == 'standard':
                outcome_col = 'outcome'
            elif model_type == 'score_based':
                outcome_col = 'scaled_outcome'
            else:
                raise ValueError("model_type should be 'standard' or 'score_based'")
            pl_matches['s'] = np.where(
                pl_matches['player'] == pl,
                    pl_matches[outcome_col],
                    1 - pl_matches[outcome_col]
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

# %% Standard Glicko 2 Ratings on Train Sets

# Women's Epee
womens_epee_pool_ratings_standard = glicko2_ratings(matches_we_pool_train, model_type = 'standard') # Pool Standard Ratings
womens_epee_de_ratings_standard = glicko2_ratings(matches_we_de_train, model_type = 'standard') # DE Standard Ratings

# Men's Epee
mens_epee_pool_ratings_standard = glicko2_ratings(matches_me_pool_train, model_type = 'standard') # Pool Standard Ratings
mens_epee_de_ratings_standard = glicko2_ratings(matches_me_de_train, model_type = 'standard') # DE Standard Ratings

# Women's Foil
womens_foil_pool_ratings_standard = glicko2_ratings(matches_wf_pool_train, model_type = 'standard') # Pool Standard Ratings
womens_foil_de_ratings_standard = glicko2_ratings(matches_wf_de_train, model_type = 'standard') # DE Standard Ratings

# Men's Foil
mens_foil_pool_ratings_standard = glicko2_ratings(matches_mf_pool_train, model_type = 'standard') # Pool Standard Ratings
mens_foil_de_ratings_standard = glicko2_ratings(matches_mf_de_train, model_type = 'standard') # DE Standard Ratings

# Women's Saber
womens_saber_pool_ratings_standard = glicko2_ratings(matches_ws_pool_train, model_type = 'standard') # Pool Standard Ratings
womens_saber_de_ratings_standard = glicko2_ratings(matches_ws_de_train, model_type = 'standard') # DE Standard Ratings

# Men's Saber
mens_saber_pool_ratings_standard = glicko2_ratings(matches_ms_pool_train, model_type = 'standard') # Pool Standard Ratings
mens_saber_de_ratings_standard = glicko2_ratings(matches_ms_de_train, model_type = 'standard') # DE Standard Ratings

# %% Score-Based Glicko 2 Ratings on Train Sets

# Women's Epee
womens_epee_pool_ratings_score_based = glicko2_ratings(matches_we_pool_train, model_type = 'score_based') # Pool Standard Ratings
womens_epee_de_ratings_score_based = glicko2_ratings(matches_we_de_train, model_type = 'score_based') # DE Standard Ratings

# Men's Epee
mens_epee_pool_ratings_score_based = glicko2_ratings(matches_me_pool_train, model_type = 'score_based') # Pool Standard Ratings
mens_epee_de_ratings_score_based = glicko2_ratings(matches_me_de_train, model_type = 'score_based') # DE Standard Ratings

# Women's Foil
womens_foil_pool_ratings_score_based = glicko2_ratings(matches_wf_pool_train, model_type = 'score_based') # Pool Standard Ratings
womens_foil_de_ratings_score_based = glicko2_ratings(matches_wf_de_train, model_type = 'score_based') # DE Standard Ratings

# Men's Foil
mens_foil_pool_ratings_score_based = glicko2_ratings(matches_mf_pool_train, model_type = 'score_based') # Pool Standard Ratings
mens_foil_de_ratings_score_based = glicko2_ratings(matches_mf_de_train, model_type = 'score_based') # DE Standard Ratings

# Women's Saber
womens_saber_pool_ratings_score_based = glicko2_ratings(matches_ws_pool_train, model_type = 'score_based') # Pool Standard Ratings
womens_saber_de_ratings_score_based = glicko2_ratings(matches_ws_de_train, model_type = 'score_based') # DE Standard Ratings

# Men's Saber
mens_saber_pool_ratings_score_based = glicko2_ratings(matches_ms_pool_train, model_type = 'score_based') # Pool Standard Ratings
mens_saber_de_ratings_score_based = glicko2_ratings(matches_ms_de_train, model_type = 'score_based') # DE Standard Ratings


# %% Win Prob Function
def win_prob(matches, ratings):
    def scale_rating_rd(ratings):
        ratings = ratings.copy()
        ratings['scaled_rating'] = (ratings['rating'] - 1500) / 173.7178
        ratings['scaled_RD'] = ratings['RD'] / 173.7178
        ratings['g_scaled_RD'] = 1 / np.sqrt(1 + (3 * ratings['scaled_RD']**2) / (np.pi**2))
        return ratings

    # Scale ratings first
    ratings = scale_rating_rd(ratings)
    
    matches = matches.copy()  # avoid modifying original DataFrame

    # Map ratings to players
    matches['player_rating'] = matches['player'].map(
        dict(zip(ratings['player'], ratings['rating']))
    )
    matches['opponent_rating'] = matches['opponent'].map(
        dict(zip(ratings['player'], ratings['rating']))
    )
    matches['rating1'] = matches['player'].map(
        dict(zip(ratings['player'], ratings['scaled_rating']))
    )
    matches['rating2'] = matches['opponent'].map(
        dict(zip(ratings['player'], ratings['scaled_rating']))
    )
    matches['g_scaled_RD2'] = matches['opponent'].map(
        dict(zip(ratings['player'], ratings['g_scaled_RD']))
    )
    
    # Compute win probability
    matches['prob_player_wins'] = 1 / (1 + np.exp(-matches['g_scaled_RD2'] * (matches['rating1'] - matches['rating2'])))

    return matches[['player','opponent','player_rating','opponent_rating','outcome','scaled_outcome','prob_player_wins']]

# %% Standard Model Matches Test Set with Win Probabilities

# Women's Epee
standard_win_prob_matches_we_pool_test = win_prob(matches_we_pool_test, womens_epee_pool_ratings_standard)  # Pool Data
standard_win_prob_matches_we_de_test = win_prob(matches_we_de_test, womens_epee_de_ratings_standard)  # DE Data

# Men's Epee
standard_win_prob_matches_me_pool_test = win_prob(matches_me_pool_test, mens_epee_pool_ratings_standard)  # Pool Data
standard_win_prob_matches_me_de_test = win_prob(matches_me_de_test, mens_epee_de_ratings_standard)  # DE Data

# Women's Foil
standard_win_prob_matches_wf_pool_test = win_prob(matches_wf_pool_test, womens_foil_pool_ratings_standard)  # Pool Data
standard_win_prob_matches_wf_de_test = win_prob(matches_wf_de_test, womens_foil_de_ratings_standard)  # DE Data

# Men's Foil
standard_win_prob_matches_mf_pool_test = win_prob(matches_mf_pool_test, mens_foil_pool_ratings_standard)  # Pool Data
standard_win_prob_matches_mf_de_test = win_prob(matches_mf_de_test, mens_foil_de_ratings_standard)  # DE Data

# Women's Saber
standard_win_prob_matches_ws_pool_test = win_prob(matches_ws_pool_test, womens_saber_pool_ratings_standard)  # Pool Data
standard_win_prob_matches_ws_de_test = win_prob(matches_ws_de_test, womens_saber_de_ratings_standard)  # DE Data

# Men's Saber
standard_win_prob_matches_ms_pool_test = win_prob(matches_ms_pool_test, mens_saber_pool_ratings_standard)  # Pool Data
standard_win_prob_matches_ms_de_test = win_prob(matches_ms_de_test, mens_saber_de_ratings_standard)  # DE Data

# %% Score-based Model Matches Test Set with Win Probabilities

# Women's Epee
score_based_win_prob_matches_we_pool_test = win_prob(matches_we_pool_test, womens_epee_pool_ratings_score_based)  # Pool Data
score_based_win_prob_matches_we_de_test = win_prob(matches_we_de_test, womens_epee_de_ratings_score_based)  # DE Data

# Men's Epee
score_based_win_prob_matches_me_pool_test = win_prob(matches_me_pool_test, mens_epee_pool_ratings_score_based)  # Pool Data
score_based_win_prob_matches_me_de_test = win_prob(matches_me_de_test, mens_epee_de_ratings_score_based)  # DE Data

# Women's Foil
score_based_win_prob_matches_wf_pool_test = win_prob(matches_wf_pool_test, womens_foil_pool_ratings_score_based)  # Pool Data
score_based_win_prob_matches_wf_de_test = win_prob(matches_wf_de_test, womens_foil_de_ratings_score_based)  # DE Data

# Men's Foil
score_based_win_prob_matches_mf_pool_test = win_prob(matches_mf_pool_test, mens_foil_pool_ratings_score_based)  # Pool Data
score_based_win_prob_matches_mf_de_test = win_prob(matches_mf_de_test, mens_foil_de_ratings_score_based)  # DE Data

# Women's Saber
score_based_win_prob_matches_ws_pool_test = win_prob(matches_ws_pool_test, womens_saber_pool_ratings_score_based)  # Pool Data
score_based_win_prob_matches_ws_de_test = win_prob(matches_ws_de_test, womens_saber_de_ratings_score_based)  # DE Data

# Men's Saber
score_based_win_prob_matches_ms_pool_test = win_prob(matches_ms_pool_test, mens_saber_pool_ratings_score_based)  # Pool Data
score_based_win_prob_matches_ms_de_test = win_prob(matches_ms_de_test, mens_saber_de_ratings_score_based)  # DE Data
# %% MAE function

def compute_mae(test_df, outcome_col='scaled_outcome', prob_col='prob_player_wins'):
    """
    Compute Mean Absolute Error between scaled outcomes and predicted win probabilities.
    
    Parameters:
        test_df (pd.DataFrame): DataFrame containing the outcome and predicted probabilities.
        outcome_col (str): Name of the column with actual scaled outcomes. Default: 'scaled_outcome'.
        prob_col (str): Name of the column with predicted probabilities. Default: 'prob_player_wins'.
        
    Returns:
        float: MAE value
    """
    outcomes = test_df[outcome_col]
    predictions = test_df[prob_col]
    
    # Drop NAs in predictions
    mask = ~predictions.isna()
    
    mae = mean_absolute_error(outcomes[mask], predictions[mask])
    return mae

# %% Standard Model Validation

# Women's Epee
womens_epee_pool_mae = compute_mae(standard_win_prob_matches_we_pool_test)  # Pool Matches
womens_epee_de_mae = compute_mae(standard_win_prob_matches_we_de_test)      # DE Matches

# Mens's Epee
mens_epee_pool_mae = compute_mae(standard_win_prob_matches_me_pool_test)  # Pool Matches
mens_epee_de_mae = compute_mae(standard_win_prob_matches_me_de_test)      # DE Matches

# Women's Foil
womens_foil_pool_mae = compute_mae(standard_win_prob_matches_wf_pool_test)  # Pool Matches
womens_foil_de_mae   = compute_mae(standard_win_prob_matches_wf_de_test)    # DE Matches

# Men's Foil
mens_foil_pool_mae = compute_mae(standard_win_prob_matches_mf_pool_test)    # Pool Matches
mens_foil_de_mae   = compute_mae(standard_win_prob_matches_mf_de_test)      # DE Matches

# Women's Saber
womens_saber_pool_mae = compute_mae(standard_win_prob_matches_ws_pool_test)  # Pool Matches
womens_saber_de_mae   = compute_mae(standard_win_prob_matches_ws_de_test)    # DE Matches

# Men's Saber
mens_saber_pool_mae = compute_mae(standard_win_prob_matches_ms_pool_test)    # Pool Matches
mens_saber_de_mae   = compute_mae(standard_win_prob_matches_ms_de_test)      # DE Matches

# Create a dictionary with all values
mae_data = {
    "Weapon": ["Epee", "Epee", "Foil", "Foil", "Saber", "Saber"],
    "Gender": ["Women", "Men", "Women", "Men", "Women", "Men"],
    "Pool MAE": [
        womens_epee_pool_mae, mens_epee_pool_mae,
        womens_foil_pool_mae, mens_foil_pool_mae,
        womens_saber_pool_mae, mens_saber_pool_mae
    ],
    "DE MAE": [
        womens_epee_de_mae, mens_epee_de_mae,
        womens_foil_de_mae, mens_foil_de_mae,
        womens_saber_de_mae, mens_saber_de_mae
    ]
}

# Convert to DataFrame
standard_mae_table = pd.DataFrame(mae_data)

# Display table
print(standard_mae_table)

# %% Score-based Model Validation
# Women's Epee
womens_epee_pool_mae = compute_mae(score_based_win_prob_matches_we_pool_test)  # Pool Matches
womens_epee_de_mae = compute_mae(score_based_win_prob_matches_we_de_test)      # DE Matches

# Men's Epee
mens_epee_pool_mae = compute_mae(score_based_win_prob_matches_me_pool_test)  # Pool Matches
mens_epee_de_mae = compute_mae(score_based_win_prob_matches_me_de_test)      # DE Matches

# Women's Foil
womens_foil_pool_mae = compute_mae(score_based_win_prob_matches_wf_pool_test)  # Pool Matches
womens_foil_de_mae   = compute_mae(score_based_win_prob_matches_wf_de_test)    # DE Matches

# Men's Foil
mens_foil_pool_mae = compute_mae(score_based_win_prob_matches_mf_pool_test)    # Pool Matches
mens_foil_de_mae   = compute_mae(score_based_win_prob_matches_mf_de_test)      # DE Matches

# Women's Saber
womens_saber_pool_mae = compute_mae(score_based_win_prob_matches_ws_pool_test)  # Pool Matches
womens_saber_de_mae   = compute_mae(score_based_win_prob_matches_ws_de_test)    # DE Matches

# Men's Saber
mens_saber_pool_mae = compute_mae(score_based_win_prob_matches_ms_pool_test)    # Pool Matches
mens_saber_de_mae   = compute_mae(score_based_win_prob_matches_ms_de_test)      # DE Matches

# Create a dictionary with all values
mae_data = {
    "Weapon": ["Epee", "Epee", "Foil", "Foil", "Saber", "Saber"],
    "Gender": ["Women", "Men", "Women", "Men", "Women", "Men"],
    "Pool MAE": [
        womens_epee_pool_mae, mens_epee_pool_mae,
        womens_foil_pool_mae, mens_foil_pool_mae,
        womens_saber_pool_mae, mens_saber_pool_mae
    ],
    "DE MAE": [
        womens_epee_de_mae, mens_epee_de_mae,
        womens_foil_de_mae, mens_foil_de_mae,
        womens_saber_de_mae, mens_saber_de_mae
    ]
}

# Convert to DataFrame
score_based_mae_table = pd.DataFrame(mae_data)

# Display table
print(score_based_mae_table)
