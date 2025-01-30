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

def fetch_publishers():
    url = "https://steam.fandom.com/wiki/List_of_Steam_games"
    driver.get(url)
    time.sleep(5)  # Wartezeit zum Laden der Seite

    publishers = []
    seen_publishers = {}  # Dictionary to track rowspan publishers

    # Finde alle Zeilen der Tabelle mit Spielen
    rows = driver.find_elements(By.CSS_SELECTOR, "table.article-table tbody tr")

    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")

        # Überprüfe, ob es genug Spalten gibt, um die Publisher zu extrahieren
        if len(columns) > 1:
            publisher = None

            # Suche nach dem Publisher in einem td mit colspan="2"
            publisher_elements = row.find_elements(By.CSS_SELECTOR, 'td[colspan="2"]')
            if publisher_elements:
                publisher = publisher_elements[0].text.strip()
                publishers.append(publisher)
                continue  # Weiter zur nächsten Zeile, wenn Publisher gefunden wurde

            # Suche nach Publishern, die über mehrere Zeilen gehen (rowspan)
            for col in columns:
                rowspan = col.get_attribute('rowspan')
                if rowspan and int(rowspan) > 1:
                    publisher_text = col.text.strip()
                    if publisher_text and publisher_text not in seen_publishers:
                        seen_publishers[publisher_text] = int(rowspan)
                        publishers.append(publisher_text)
                        break  # Publisher gefunden, gehe zur nächsten Zeile

            # Falls der Publisher weder unter colspan noch rowspan gefunden wurde,
            # versuche ihn direkt aus der Zelle zu extrahieren
            if not publisher:
                for col in columns:
                    if not col.get_attribute('colspan') and not col.get_attribute('rowspan'):
                        publisher = col.text.strip()
                        if publisher:
                            publishers.append(publisher)
                            break  # Wenn Publisher gefunden, gehe zur nächsten Zeile

    return publishers

def save_to_excel(data, filename):
    df = pd.DataFrame(data, columns=["Publisher"])
    df.to_excel(filename, index=False, engine="openpyxl")
    os.startfile(filename)  # Öffne die Datei direkt

if __name__ == '__main__':
    print("Fetching publishers from Steam Fandom...")
    publishers = fetch_publishers()

    print(f"Gefundene Publisher: {len(publishers)}")
    print(publishers[:5])  # Zeige die ersten 5 Einträge

    output_file = "steam_publishers.xlsx"
    print(f"Saving data to {output_file}...")
    save_to_excel(publishers, output_file)

    print("Done!")
    driver.quit()
