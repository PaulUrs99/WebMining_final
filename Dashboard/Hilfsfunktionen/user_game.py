import requests
import json
import sys

def fetch_in_game_data(api_key, steam_id, app_id):
    
    url = "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
    
    params = {
        'key': api_key,
        'steamid': steam_id,
        'appid': app_id
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Löst eine Exception aus, wenn Statuscode != 200
        
        data = response.json()
        playerstats = data.get("playerstats", {})
        
        # Überprüfen, ob 'stats' in 'playerstats' vorhanden ist
        if "stats" in playerstats:
            stats = playerstats["stats"]
            # Liste aus Dictionaries erstellen
            stats_list = []
            for stat in stats:
                stats_list.append({
                    "name": stat.get("name"),
                    "value": stat.get("value")
                })

            # Rückgabe in einem Struct/Dictionary, damit wir erkennen, ob alles OK ist
            return {
                "status": "success",
                "stats": stats_list
            }
        else:
            return {
                "status": "error",
                "message": "Keine Statistiken gefunden oder das Profil ist privat."
            }
            
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP-Fehler aufgetreten: {http_err}")
    except Exception as err:
        print(f"Ein unbekannter Fehler ist aufgetreten: {err}")

if __name__ == "__main__":
    # Prüfen, ob alle 3 Argumente übergeben wurden <API_KEY> <STEAM_ID64> <APP_ID>
    if len(sys.argv) != 4:
        print(f"Verwendung: python {sys.argv[0]} <API_KEY> <STEAM_ID64> <APP_ID>")
        sys.exit(1)

    api_key_arg = sys.argv[1]
    steam_id_arg = sys.argv[2]
    app_id_arg = sys.argv[3]

    fetch_in_game_data(api_key_arg, steam_id_arg, app_id_arg)