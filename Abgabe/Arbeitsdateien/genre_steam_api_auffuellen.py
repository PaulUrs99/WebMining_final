import requests
import pandas as pd
import time
import random
import concurrent.futures

for i in range(150):
    # Datei mit den ursprünglichen Genres laden
    file_path = "steam_game_genres.csv"
    df_genres = pd.read_csv(file_path)
    # **Nur für Spiele ohne Genre erneut API-Aufrufe durchführen**
    missing_games = df_genres[df_genres['genres'].isna()]['appid'].tolist()

    if missing_games:

        # Basis-URL für die Steam Store API
        API_BASE_URL = "https://store.steampowered.com/api/appdetails?appids="

        # Funktion zum Abrufen der Genres für eine App-ID
        def get_game_details(appid):
            url = f"{API_BASE_URL}{appid}"
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                if str(appid) in data and data[str(appid)]['success']:
                    genres = data[str(appid)]['data'].get('genres', [])
                    genre_list = ', '.join([genre['description'] for genre in genres])
                    return genre_list if genre_list else None
            except requests.exceptions.RequestException:
                return None
            return None


        # Fortschrittszähler
        total_missing = len(missing_games)
        processed = 0

        def fetch_missing_genres(appid):
            global processed
            genre = get_game_details(appid)
            
            # Update des DataFrame
            df_genres.loc[df_genres['appid'] == appid, 'genres'] = genre

            # Fortschritt ausgeben
            processed += 1
            if processed % 100 == 0 or processed == total_missing:
                print(f"🔄 {processed}/{total_missing} Spiele verarbeitet...")

            return {'appid': appid, 'genres': genre}

        # Multi-Threading für parallele API-Anfragen
        if missing_games:
            print(f"🚀 Starte das Update für {total_missing} Spiele ohne Genre...")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                list(executor.map(fetch_missing_genres, missing_games))

            # Speichern der aktualisierten Datei
            df_genres.to_csv(file_path, index=False)

            # Abschlussbericht
            remaining_missing = df_genres['genres'].isna().sum()
            filled_count = total_missing - remaining_missing

            print(f"✅ Update abgeschlossen: {filled_count} Genres ergänzt.")
            print(f"❗ Noch {remaining_missing} Spiele haben kein Genre.")
        else:
            print("✅ Alle Spiele haben bereits ein Genre! Kein Update nötig.")
    else:
        break