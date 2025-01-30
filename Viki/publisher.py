import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

def fetch_steam_games():
    url = "https://steam.fandom.com/wiki/List_of_Steam_games"
    driver.get(url)
    time.sleep(5)  # Wartezeit zum Laden der Seite

    titles = []

    # Finde die Tabelle mit Spielen
    rows = driver.find_elements(By.CSS_SELECTOR, "table.article-table tbody tr")

    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")

        if len(columns) >= 1:
            # Versuche, den title aus <span class="new"> zu holen
            game_elements = columns[0].find_elements(By.CSS_SELECTOR, "span.new")
            if game_elements:
                game_title = game_elements[0].get_attribute("title").strip()  # Holen des title Attributs
                titles.append(game_title)

    return titles


def save_to_excel(data, filename):
    df = pd.DataFrame(data, columns=["Title"])
    df.to_excel(filename, index=False, engine="openpyxl")
    os.startfile(filename)  # Öffne die Datei direkt

if __name__ == '__main__':
    print("Fetching titles from Steam Fandom...")
    titles = fetch_steam_games()

    print(f"Gefundene Titel: {len(titles)}")
    print(titles[:5])  # Zeige die ersten 5 Einträge

    output_file = "steam_titles.xlsx"
    print(f"Saving data to {output_file}...")
    save_to_excel(titles, output_file)

    print("Done!")
    driver.quit()
