import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# CSV-Datei einlesen
csv_file = r'C:\Viki\Desktop\WebMining\Viki\unique_games.csv'
games_data = pd.read_csv(csv_file)

# Sicherstellen, dass die Spalte 'genre' existiert
if 'genre' not in games_data.columns:
    games_data['genre'] = None  # Neue Spalte hinzufügen, falls nicht vorhanden

# Selenium Optionen setzen
chrome_options = Options()
chrome_options.add_argument('--headless')  
chrome_options.add_argument('--disable-gpu')  # Hilft bei einigen Systemen


# chrome_options.add_argument('--headless')  # Falls kein sichtbares Browserfenster benötigt wird

driver = webdriver.Chrome(options=chrome_options)

# Webseite öffnen
driver.get('https://gamalytic.com/game-list?genres=Action')
time.sleep(10)  # Warten, bis die Seite vollständig geladen ist

try:
    # Über alle Namen in der CSV iterieren
    for index, row in games_data.iterrows():
        game_name = row['name']
        print(f'Suche nach: {game_name}')
        
        # Suchfeld finden
        search_input = driver.find_element(By.XPATH, "//input[@name='title']")
        
        # Sicherstellen, dass das Suchfeld geleert wird
        search_input.clear()
        search_input.send_keys(Keys.CONTROL + "a")  # Text markieren
        search_input.send_keys(Keys.DELETE)  # Markierten Text löschen
        
        # Namen eingeben und Suche abschicken
        search_input.send_keys(game_name)  # Namen eingeben
        search_input.send_keys(Keys.RETURN)  # Suche abschicken
        
        time.sleep(5)  # Warten, bis die Suchergebnisse geladen sind

        try:
            # Überprüfen, ob ein Ergebnis existiert
            first_value_element = driver.find_element(By.CSS_SELECTOR, '#__next > div > main > div.MuiBox-root.css-1svywxg > div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.css-isbt42 > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-true.css-kxu0dz > div > div > div > div > div.MuiDataGrid-main.css-opb0c2 > div:nth-child(2) > div > div > div > div:nth-child(1) > div:nth-child(1) > a')
            first_value = first_value_element.text
            
            print(f'Gefundener Eintrag: {first_value}')
            
            # Spalte 'genre' mit 'action' aktualisieren
            games_data.loc[index, 'genre'] = 'action'
        except Exception as e:
            print(f'Kein Ergebnis für {game_name}: {e}')
        
        time.sleep(0)  # Kurze Pause zwischen den Suchanfragen

finally:
    # Browser schließen
    driver.quit()

# Aktualisierte CSV-Datei speichern
output_file = r'C:\Viki\Desktop\WebMining\Viki\unique_games_updated.csv'
games_data.to_csv(output_file, sep=';', index=False)
print(f'Aktualisierte Datei wurde in "{output_file}" gespeichert.')
