import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Chrome-Options konfigurieren
chrome_options = Options()
# Optional: Browser im Headless-Modus ausführen
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

# WebDriver initialisieren
driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(60)  # Ladezeit-Timeout auf 60 Sekunden setzen
driver.implicitly_wait(10)       # Implizites Warten auf 10 Sekunden setzen

try:
    # Website öffnen
    driver.get('https://www.gamestar.de/releaseliste/')
    time.sleep(5)  # Wartezeit für die initiale Seitenladung

    # Scrollen mit Fehlerbehandlung
    for _ in range(20):
        try:
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1)
        except Exception as e:
            print(f"Fehler beim Scrollen: {e}")
            break

    # Spiele-Daten extrahieren
    game_elements = driver.find_elements(By.CSS_SELECTOR, 'div.div-table.responsive')
    games = []
    for game in game_elements:
        try:
            h2_element = game.find_element(By.CSS_SELECTOR, 'h2.responsive.align-top.m-b-0.h3')
            title = h2_element.find_element(By.TAG_NAME, 'a').text
            link = h2_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            games.append({'title': title, 'link': link})
        except Exception as e:
            print(f"Fehler beim Extrahieren eines Spiels: {e}")

    # Daten in CSV speichern
    df = pd.DataFrame(games)
    if not df.empty:
        df.to_csv('gamestar_releases.csv', sep=';', index=False)
        print("Daten wurden erfolgreich in 'gamestar_releases.csv' gespeichert.")
    else:
        print("Keine Daten gefunden. Bitte überprüfe die Selektoren oder die Webseite.")

finally:
    driver.quit()
