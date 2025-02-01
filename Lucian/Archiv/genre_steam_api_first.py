import requests
import pandas as pd
import time
import random
import concurrent.futures

# Datei mit Spiele-Daten (falls noch nicht im DataFrame vorhanden)
file_path = "filtered_games.csv"
df_filtered_games = pd.read_csv(file_path)

# Einzigartige App-IDs extrahieren
unique_appids = df_filtered_games['appid'].unique()

# Basis-URL für die Steam Store API
API_BASE_URL = "https://store.steampowered.com/api/appdetails?appids="

# Funktion zum Abrufen der Genres für eine App-ID
def get_game_details(appid):
    url = f"{API_BASE_URL}{appid}"
    try:
        response = requests.get(url, timeout=5)  # 5 Sekunden Timeout
        response.raise_for_status()
        data = response.json()
        if str(appid) in data and data[str(appid)]['success']:
            genres = data[str(appid)]['data'].get('genres', [])
            genre_list = ', '.join([genre['description'] for genre in genres])
            return {'appid': appid, 'genres': genre_list}
    except requests.exceptions.RequestException:
        return {'appid': appid, 'genres': None}  # Falls Fehler, None zurückgeben
    return {'appid': appid, 'genres': None}

# Multi-Threading für parallele API-Anfragen
def fetch_all_games(appids, num_threads=20):
    game_genre_data = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = executor.map(get_game_details, appids)
    
        for idx, result in enumerate(results):
            game_genre_data.append(result)
            if (idx + 1) % 100 == 0:
                print(f"{idx+1}/{len(appids)} Spiele verarbeitet...")

    return game_genre_data

# API-Anfragen parallel ausführen
start_time = time.time()
game_genre_data = fetch_all_games(unique_appids, num_threads=20)
end_time = time.time()

# Speichern der Ergebnisse
df_genres = pd.DataFrame(game_genre_data)
df_genres.to_csv("steam_game_genres.csv", index=False)

print(f"Fertig! Die Genre-Daten wurden gespeichert.")
print(f"Dauer: {round(end_time - start_time, 2)} Sekunden")
