# H2H Matchup Dashboard with Score-based Glicko-2 Rating Model for Fencing

<div style="text-align: justify;">

This project presents a **Head-to-Head (H2H) analytics dashboard** for the **Philippine Fencing Association (PFA) National Rankings**, covering **all three weapons in each category (Men’s and Women’s Épée, Foil, and Sabre)**.

The system combines **web-scraped bout-level data**, a **score-based Glicko-2 rating model**, and an **interactive Streamlit dashboard** to enable direct comparisons between any two fencers. Unlike traditional win/loss rating systems, this implementation incorporates **margin of victory** to better reflect match dominance and competitive intensity, particularly important in fencing where score differentials carry meaningful information.

The dashboard allows users to compare two fencers’ pool and direct elimination (DE) performance, view separate Glicko-2 ratings for pools and DE bouts, examine head-to-head history, and generate probabilistic match predictions while explicitly accounting for rating uncertainty.

</div>

---

## Data Sources

<div style="text-align: justify;">

This project uses official tournament data from the **Philippine Fencing Association (PFA) National Rankings**, scraped directly from **FencingTimeLive**. Each dataset corresponds to **five legs of a national ranking season per weapon**.

</div>

Example data sources:
- [FencingTimeLive – PFA National Rankings](https://www.fencingtimelive.com/)

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

## Model Building

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
- `glicko2_model.py`

---

## Dashboard Implementation

<div style="text-align: justify;">

The interactive dashboard was developed using **Streamlit**, with **Plotly** used for all visualizations. The interface supports weapon- and c
