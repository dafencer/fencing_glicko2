# Head-to-Head Match Outcome Prediction for Philippine Fencing Rankings Using a Score-Based Glicko-2 Model

<div style="text-align: justify;">

This project presents a **Head-to-Head (H2H) analytics dashboard** for the **Philippine Fencing Association (PFA) Senior Rankings**, covering **all three weapons in each category (Men’s and Women’s Épée, Foil, and Sabre)**.

The system combines **web-scraped bout-level data**, a **score-based Glicko-2 rating model**, and an **interactive Streamlit dashboard** to enable direct comparisons between any two fencers. Unlike traditional win/loss rating systems, this implementation incorporates **margin of victory** to better reflect match dominance and competitive intensity, particularly important in fencing where score differentials carry meaningful information.

The dashboard allows users to compare two fencers’ pool and direct elimination (DE) performance, view separate Glicko-2 ratings for pools and DE bouts, examine head-to-head history, and generate probabilistic match predictions while explicitly accounting for rating uncertainty.

<img width="1710" height="975" alt="image" src="https://github.com/user-attachments/assets/6a71c3d7-7fde-486a-9e99-5ba0da22d8f4" />
<img width="1710" height="981" alt="image" src="https://github.com/user-attachments/assets/1c654be4-c630-4f10-b3ae-7c9364c4ed97" />



</div>

---

## Data Sources

<div style="text-align: justify;">

This project uses official tournament data from the **Philippine Fencing Association (PFA) Senior Rankings**, scraped directly from **FencingTimeLive**. Each dataset corresponds to **five legs of a national ranking season per weapon**.

</div>

Example data sources:
- [1st Leg PFA Senior Rankings- Women's Epee](https://www.fencingtimelive.com/events/results/BC6BB9DF4F3C4698ABC67C7C981EA492)
- [1st Leg PFA Senior Rankings- Women's Foil](https://www.fencingtimelive.com/events/results/EF4AD5BC76F44A92938E9BF8A4382B99)
- [1st Leg PFA Senior Rankings- Women's Saber](https://www.fencingtimelive.com/events/results/D67D97E1E0624E60AFE6BD65D60E1671)
- [1st Leg PFA Senior Rankings- Men's Epee](https://www.fencingtimelive.com/events/results/76CB0AD0E6CE46BE9AF6C1B22A547E75)
- [1st Leg PFA Senior Rankings- Men's Foil](https://www.fencingtimelive.com/events/results/1E4CF552A0894276ADC15A6ECEB579C3)
- [1st Leg PFA Senior Rankings- Men's Saber](https://www.fencingtimelive.com/events/results/127C9B14E0A24F2A824030C5AC81675B)

Separate datasets were collected for:
- Pool bouts  
- Direct Elimination (DE) tableau bouts  

---

## Data Collection

<div style="text-align: justify;">

All match data were collected via **automated web scraping** using **Selenium (Python)**. Two dedicated scrapers were developed: one for **pool matches** and one for **direct elimination bouts**.

The scraping pipeline iterates across all tournament legs, extracts fencer names, scores, round information, and winners, and handles multi-round DE tableaux with dynamic spacing logic. The output consists of consolidated CSV files generated separately for each weapon and category.

</div>

Relevant scripts:
- `web scrape (pools).py`
- `web scrape (DE).py`

---

## Data Cleaning

<div style="text-align: justify;">

Raw scraped data were cleaned and standardized to produce a unified bout-level dataset. Cleaning steps included parsing score formats (e.g., `V5`, `15–12`), removing bye rounds and invalid DE entries, standardizing fencer name formats, separating pool and DE matches, and merging all tournament legs into a single dataset.

Additional computed fields were added, including **margin of victory (MOV)** and **scaled outcomes** derived from score differentials. The scaled outcome is defined as:

</div>

$$ \text{Scaled Outcome} = 0.5 + \frac{\text{Margin of Victory}}{2 \times \text{Winning Score}} $$

<div style="text-align: justify;">

This transformation enables the Glicko-2 model to incorporate not only match outcomes but also the **degree of dominance** displayed in each bout.

</div>

Relevant script:
- `data_cleaning.py`

---

## Model Building and Validation

<div style="text-align: justify;">

A **custom score-based Glicko-2 rating model** was implemented from first principles in Python, following the official Glicko-2 framework while extending it to support margin-aware outcomes.

Instead of binary win–loss results, the model processes **scaled outcomes** derived from margin of victory. Matches are grouped into rating periods aligned with tournament legs, and each fencer’s **rating**, **rating deviation (RD)**, and **volatility** are updated accordingly.

</div>

Two independent rating systems were computed:
- **Pool Glicko-2 Ratings**
- **Direct Elimination (DE) Glicko-2 Ratings**

<div style="text-align: justify;">

This separation reflects structural differences between pool bouts (shorter, round-robin format) and DE matches (longer, elimination-based), allowing for more accurate performance modeling.

</div>

Relevant script:
- Model Validation: `model.py`
- Final Model Implementation: `glicko2.py`

---

## Dashboard Implementation

<div style="text-align: justify;">

The interactive dashboard was developed using **Streamlit**, with **Plotly** used for all visualizations. The interface supports weapon- and category-specific pages, enabling users to select any two fencers and view side-by-side comparisons.

Displayed information includes Glicko-2 ratings, rating deviations, head-to-head history, and probabilistic win predictions. Prediction probabilities are computed using the standard Glicko-2 expected score formulation, with ratings transformed into Glicko-2 scale space and evaluated separately for pool and DE contexts.

</div>

Relevant components:
- `Home.py`
- Weapon-specific pages (e.g., `Women's_Epee.py`, `Men's_Foil.py`)
- Shared styling and utility functions

---

## Evaluation

<div style="text-align: justify;">

The score-based Glicko-2 model produces more informative and stable ratings than traditional win–loss systems. By incorporating margin of victory, the model distinguishes dominant performances from narrow wins while maintaining appropriate uncertainty for fencers with limited match histories.

Separating pool and DE ratings reveals meaningful competitive patterns, highlighting fencers who perform consistently in pools but underperform in elimination bouts, as well as those who peak during DE matches.

</div>

---

## Future Work

<div style="text-align: justify;">

Planned extensions to this project include time-decay weighting for recent performances, cross-weapon normalization, tournament-level match simulations, integration of seeding effects, and deployment of a public-facing dashboard. Further validation against international ranking systems is also planned. Additionally, the model can be extended to implement predictions for **team events**, allowing comparisons and outcome estimations for national teams based on aggregated individual performances.


</div>

---

## Acknowledgments / References

- [Philippine Fencing Association (PFA)](https://phil-fencing.com/)  
- [FencingTimeLive]((https://www.fencingtimelive.com/)) for tournament data access  
- Glickman, M. E. (2012). *[The Glicko-2 System](https://www.glicko.net/glicko/glicko2.pdf)*  
- Streamlit and Plotly open-source communities
