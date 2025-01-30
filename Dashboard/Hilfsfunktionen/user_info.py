import requests
from datetime import datetime # Umwandlung von UNIX-Timestamp in lesbares Format (lastlogoff & timecreated)

def get_user_info(api_key, steam_id):

    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"

    params = {
        "key": api_key,
        "steamids": steam_id
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Überprüfen, ob Daten vorhanden sind
        if "response" in data and "players" in data["response"] and len(data["response"]["players"]) > 0:
            player_info = data["response"]["players"][0]  # Es wird nur ein Spieler abgefragt

            # Überprüfen, ob lastlogoff und timecreated verfügbar sind
            if "lastlogoff" in player_info:
                lastlogoff_readable = datetime.utcfromtimestamp(player_info["lastlogoff"]).strftime('%Y-%m-%d %H:%M:%S')
            else:
                lastlogoff_readable = "Nicht verfügbar"

            if "timecreated" in player_info:
                timecreated_timestamp = player_info["timecreated"]
                timecreated_readable = datetime.utcfromtimestamp(timecreated_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                
                # Berechnung der Tage seit der Kontoerstellung
                today = datetime.utcnow()  # Aktuelles UTC-Datum
                days_since_creation = (today - datetime.utcfromtimestamp(timecreated_timestamp)).days
            else:
                timecreated_readable = "Nicht verfügbar"
                days_since_creation = "Nicht verfügbar"

            return {
                "personaname": player_info.get("personaname", "N/A"),
                "avatarfull": player_info.get("avatarfull", "N/A"),
                "lastlogoff": lastlogoff_readable,
                "timecreated": timecreated_readable,
                "days_since_creation": days_since_creation
            }
        else:
            return {"error": "Keine Daten für die angegebene SteamID gefunden."}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
