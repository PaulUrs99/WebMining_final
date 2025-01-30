import requests

def get_user_stats_for_game(api_key, steam_id, app_id):
    """
    Fetches the user statistics for a specific game.
    """
    url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"

    params = {
        'key': api_key,
        'steamid': steam_id,
        'appid': app_id
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'playerstats' in data and 'stats' in data['playerstats']:
            return data['playerstats']['stats']
        else:
            return {"error": "Keine Statistiken gefunden oder Profil ist privat."}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}