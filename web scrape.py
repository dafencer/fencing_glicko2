import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# List of URLs for all legs
leg_urls = [
    'https://www.fencingtimelive.com/events/results/BC6BB9DF4F3C4698ABC67C7C981EA492',  # Leg 1
    'https://www.fencingtimelive.com/events/results/E04B7C8376F44EB9802B73BE4BF12F4E',  # Leg 2
    'https://www.fencingtimelive.com/events/results/7F980738E0144C8DAA418ECB7FBE3124',  # Leg 3
    'https://www.fencingtimelive.com/events/results/CE92CC2A35D341FB8FF98A33F8674355',  # Leg 4
    'https://www.fencingtimelive.com/events/results/2434850A79B148CC9608A0935CB5274E',  # Leg 5
]

path = '/Users/dancanlas/chromedriver-mac-x64/chromedriver'

options = Options()
options.add_experimental_option("detach", True)
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

all_bouts = []  # Master list for all legs

for leg_index, website in enumerate(leg_urls, start=1):
    driver.get(website)

    # Head over to the Pools tab
    pools_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Pools')]"))
    )
    pools_button.click()

    # Find all Details buttons
    details_buttons = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn.btn-primary.btn-sm"))
    )
    print(f"Leg {leg_index}: Found {len(details_buttons)} Details buttons")

    # Loop through each Details button
    for i in range(len(details_buttons)):
        details_buttons = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn.btn-primary.btn-sm"))
        )
        link = details_buttons[i].get_attribute("href")

        # Open Details page in new tab
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[1])

        # Find Bout Order table
        tables = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table")))
        bout_table = None
        for table in tables:
            header_cells = table.find_elements(By.TAG_NAME, "th")
            headers = [cell.text.strip() for cell in header_cells]
            if "Right Fencer" in headers and "Left Fencer" in headers:
                bout_table = table
                break

        # Extract rows
        if bout_table:
            table_rows = bout_table.find_elements(By.TAG_NAME, "tr")
            for row in table_rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells and len(cells) >= 5:
                    right_fencer = cells[1].text.strip()
                    score1 = cells[2].text.strip()
                    score2 = cells[3].text.strip()
                    left_fencer = cells[4].text.strip()
                    pool_number = i + 1
                    all_bouts.append([leg_index, pool_number, right_fencer, score1, score2, left_fencer])

        # Close tab and return to main page
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.5)

# Convert all bouts to a single DataFrame
all_legs_df = pd.DataFrame(
    all_bouts,
    columns=["Leg", "Pool", "Right Fencer", "Score1", "Score2", "Left Fencer"]
)

# Save to CSV if desired
all_legs_df.to_csv("all_legs_pool_bouts.csv", index=False)

# Close browser
driver.quit()

print("Scraping complete! Combined DataFrame created.")
