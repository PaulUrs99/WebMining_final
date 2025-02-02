import requests
import json

def get_owned_games(api_key, steam_id, app_id):
    url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"

    params = {
        'key': api_key,
        'steamid': steam_id,
        'appid': app_id
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'playerstats' in data and 'stats' in data['playerstats']:
            stats = data['playerstats']['stats']
            print(f"Statistiken für Spiel {app_id}:")
            
            for stat in stats:
                print(f"{stat['name']}: {stat['value']}")


        else:
            print("Keine Stastics gefunden oder Profil ist privat.")
    else:
        print(f"Fehler beim Abrufen der Daten. Statuscode: {response.status_code}")

if __name__ == "__main__":
    # Replace these placeholders with actual values
    API_KEY = "DB15759E609C1E342536A6973593A57F"
    STEAM_ID = "76561198080617859"
    APP_ID = "730"

    #76561198990374557 - paul.u1111
    #76561198254607847 - ImRizzex
    #76561198080617859 - ConCHEATER Wurst (Leopold Stotch)
    #76561197979048211 - floblak3
    #76561198364896644 - Yoink (Nathan)
    #76561198059410849 - jdvmb (viki)
    #76561198286398265 - theo_o (Daniel)

    #Spiele: Counter-Strike 2 (730 - viele Statistiken), Baldur's Gate 3 (1086940 - wenige Statistiken)
    #Spiele: PUGB: Battleground (578080 - wenige Statistiken), Among Us (945360 - keine Statistiken), Counter-Strike: Source (240 - viele Statistiken)

    get_owned_games(API_KEY, STEAM_ID, APP_ID)
