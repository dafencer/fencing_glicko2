import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------- Configuration ----------
leg_urls = [
    'https://www.fencingtimelive.com/events/results/76CB0AD0E6CE46BE9AF6C1B22A547E75',  # Leg 1
    'https://www.fencingtimelive.com/events/results/0E6F31D1879040ACB84288D975710BB7',  # Leg 2
    'https://www.fencingtimelive.com/events/results/E1A37665E3534B2AB4EBF3B0951A6476',  # Leg 3
    'https://www.fencingtimelive.com/events/results/BE76E6461BC34C10BAB2DE65EDA8B402',  # Leg 4
    'https://www.fencingtimelive.com/events/results/EEDC2FC470A54936B2574310C5351AA3',  # Leg 5
]
chromedriver_path = '/Users/dancanlas/chromedriver-mac-x64/chromedriver'

options = Options()
options.add_experimental_option("detach", True)  # Keep browser open
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

all_bouts = []

for leg_index, url in enumerate(leg_urls, start=1):
    driver.get(url)
    
    # Maximize browser to ensure full table is visible
    driver.maximize_window()
    time.sleep(1)

    # Click the "Tableau" tab
    tableau_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Tableau')]"))
    )
    tableau_button.click()
    time.sleep(1)  # wait for tab to render

    # Click Full Screen Tableau button if exists
    try:
        full_screen_btn = driver.find_element(By.CSS_SELECTOR, "button.fullscreen")  # update selector if needed
        full_screen_btn.click()
        time.sleep(2)  # wait for table to expand
    except:
        print("Full screen button not found, continuing")

    # Wait for table rows and scores to load
    bout_table = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
    )
    wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
    )

    table_cols = bout_table.find_elements(By.TAG_NAME, "th")
    table_rows = bout_table.find_elements(By.TAG_NAME, "tr")

    max_rounds = len(table_cols)
    for a in range(max_rounds):
        spacing = 4 * (2 ** a)
        for i in range(1 + 2**a, len(table_rows), spacing):
            try:
                if i + (1 + 2**a) >= len(table_rows):
                    continue
                if i + 2**(a+1) >= len(table_rows):
                    continue

                row1 = table_rows[i]
                row3 = table_rows[i + 2**(a+1)]
                scorerow = table_rows[i + (1 + 2**a)]
                winnerrow = table_rows[(i-1) + (1 + 2**a)]

                # Right fencer
                try:
                    r_fencer_last = row1.find_element(By.CSS_SELECTOR, "span.tcln").text.strip()
                except:
                    r_fencer_last = ""
                try:
                    r_fencer_first = row1.find_element(By.CSS_SELECTOR, "span.tcfn").text.strip()
                except:
                    r_fencer_first = ""
                right_fencer = f"{r_fencer_last} {r_fencer_first}".strip()

                # Left fencer
                try:
                    l_fencer_last = row3.find_element(By.CSS_SELECTOR, "span.tcln").text.strip()
                except:
                    l_fencer_last = ""
                try:
                    l_fencer_first = row3.find_element(By.CSS_SELECTOR, "span.tcfn").text.strip()
                except:
                    l_fencer_first = ""
                left_fencer = f"{l_fencer_last} {l_fencer_first}".strip()

                # Extract score, ignoring time/referee spans
                scorerow_cells = scorerow.find_elements(By.TAG_NAME, "td")

                score_cell = ""  # default empty
                for td in scorerow_cells:
                    tsco_spans = td.find_elements(By.CSS_SELECTOR, "span.tsco")
                    if tsco_spans:  # if found at least one
                        score_cell = tsco_spans[0].text.strip()
                        break  # take the first one and stop
               

                # winner
                try:
                    w_fencer_last = winnerrow.find_element(By.CSS_SELECTOR, "span.tcln").text.strip()
                except:
                    w_fencer_last = ""
                try:
                    w_fencer_first = winnerrow.find_element(By.CSS_SELECTOR, "span.tcfn").text.strip()
                except:
                    w_fencer_first = ""
                winner = f"{w_fencer_last} {w_fencer_first}".strip()

    
                round_names = [th.text.strip() for th in table_cols if th.text.strip()][a]
                all_bouts.append([leg_index, round_names, right_fencer, left_fencer, score_cell, winner])

            except IndexError:
                continue

# ---------- Convert to DataFrame ----------
df = pd.DataFrame(
    all_bouts,
    columns=["Leg", "Round", "Right Fencer", "Left Fencer", "Score", "Winner"]
)

df.to_csv("Men's Epee datasets/all_legs_de_bouts_me.csv", index=False)

# Close browser
driver.quit()

print("Scraping complete! DataFrame created.")
df
