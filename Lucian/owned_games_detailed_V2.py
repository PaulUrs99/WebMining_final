import requests
import json
import pandas as pd
import os

def get_owned_games(api_key, steam_id, include_appinfo=True, include_played_free_games=True):
    """
    Fetches the owned games of a Steam user using the Steam Web API.

    :param api_key: Your Steam Web API key (string).
    :param steam_id: The SteamID64 of the user (string).
    :param include_appinfo: Whether to include app info (default: True).
    :param include_played_free_games: Whether to include free games (default: False).
    :return: JSON response with the list of owned games or an error message.
    """
    base_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"

    params = {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": str(include_appinfo).lower(),
        "include_played_free_games": str(include_played_free_games).lower(),
        "format": "json"
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 429:
            print("Error 429. API rate limit exceeded. Please wait and try again later.")
            return {"error": "API rate limit exceeded."}

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def update_csv(steam_id, games_data, output_csv):
    """
    Updates the CSV file with the fetched game data.
    """
    # Neue Spiele hinzufügen
    new_entries = []
    for game in games_data:
        appid = game.get("appid")
        name = game.get("name", "Unknown")
        playtime_forever = game.get("playtime_forever", 0)
        playtime_2weeks = game.get("playtime_2weeks", 0)
        has_community_visible_stats = game.get("has_community_visible_stats", False)
        new_entries.append({
            "steam_64_id": steam_id,
            "appid": appid,
            "name": name,
            "playtime_forever": playtime_forever,
            "playtime_2weeks": playtime_2weeks,
            "has_community_visible_stats": has_community_visible_stats
        })

    # Erstelle DataFrame für neue Spiele
    new_entries_df = pd.DataFrame(new_entries)

    # CSV speichern (Anhängen an bestehende Datei oder neue Datei erstellen)
    if os.path.exists(output_csv):
        new_entries_df.to_csv(output_csv, mode='a', header=False, index=False)
    else:
        new_entries_df.to_csv(output_csv, index=False)

    print(f"Spiele von Steam-ID {steam_id} wurden zu {output_csv} hinzugefügt.")

if __name__ == "__main__":
    API_KEY = "F06E65C071B7ABDE4CE3B531A06123E2"
    INPUT_CSV = "steam_friends.csv" 
    EXISTING_CSV = "owned_games_detailed.csv"
    NEW_CSV = "owned_games_detailed_2.csv"

    try:
        # Lese die Steam-IDs aus der Input-CSV
        steam_ids_df = pd.read_csv(INPUT_CSV)

        # Prüfe bereits verarbeitete IDs aus beiden Dateien
        processed_ids = set()
        if os.path.exists(EXISTING_CSV):
            existing_data = pd.read_csv(EXISTING_CSV)
            processed_ids.update(existing_data['steam_64_id'])

        if os.path.exists(NEW_CSV):
            new_data = pd.read_csv(NEW_CSV)
            processed_ids.update(new_data['steam_64_id'])

        # Schleife über jede Steam-ID aus der Eingabedatei
        for steam_id in steam_ids_df['friend_id']:
            if steam_id in processed_ids:  
                print(f"Skipping already processed Steam ID: {steam_id}")
                continue 

            print(f"Abfrage für Steam-ID: {steam_id}")
            result = get_owned_games(API_KEY, str(steam_id))

            if result.get("error") == "API rate limit exceeded.":
                break

            if "error" in result:
                print(f"Fehler bei der Abfrage für Steam-ID {steam_id}: {result['error']}")
            else:
                games_data = result.get('response', {}).get('games', [])
                print(f"Steam-ID {steam_id} besitzt {len(games_data)} Spiele.")

                # Ergebnisse in der neuen Datei speichern
                update_csv(steam_id, games_data, NEW_CSV)

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
