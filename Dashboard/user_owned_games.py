import requests
import pandas as pd

def get_owned_games(api_key, steam_id, include_appinfo=True, include_played_free_games=False):
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
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
# Browser-Debugging: http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=DEIN_API_KEY&steamid=DEINE_STEAMID64&include_appinfo=true&include_played_free_games=false&format=json