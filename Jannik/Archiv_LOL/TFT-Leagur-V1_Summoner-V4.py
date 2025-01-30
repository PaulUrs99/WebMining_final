import requests
import csv
import time

def get_tft_league_data(api_key, region, tier):
    # URL für die TFT-League-V1 API
    url = f"https://{region}.api.riotgames.com/tft/league/v1/{tier}"

    # Header mit API-Key
    headers = {
        "X-Riot-Token": api_key
    }

    # Anfrage an die API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Fehler: {response.status_code}")
        print("Antwort:", response.text)
        return None

def get_summoner_name(api_key, region, summoner_id):
    # URL für die Summoner-V4 API
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"

    # Header mit API-Key
    headers = {
        "X-Riot-Token": api_key
    }

    while True:  # Wiederhole die Anfrage, bis sie erfolgreich ist
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('name', 'Unknown')
        elif response.status_code == 429:  # Rate Limit überschritten
            print("Rate-Limit überschritten. Wartezeit beginnt...")
            wait_time = 120  # 2 Minuten warten
            for remaining in range(wait_time, 0, -1):
                print(f"Wartezeit: {remaining} Sekunden", end="\r")
                time.sleep(1)
            print("\nFortsetzen der Abfrage...")
        else:
            print(f"Fehler beim Abrufen des Summoner-Namens: {response.status_code}")
            print("Antwort:", response.text)
            return 'Unknown'
    time.sleep(1)  # Verzögerung, um zukünftige Limits zu vermeiden

def save_to_csv(data_list, filename, api_key, region):
    # CSV-Header definieren
    headers = ["Summoner Name", "Rank", "LP", "Wins", "Losses"]
    name_cache = {}

    # Daten in die CSV schreiben
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for data in data_list:
            rank = data['rank']
            for entry in data['entries']:
                summoner_id = entry.get('summonerId')
                if summoner_id in name_cache:
                    summoner_name = name_cache[summoner_id]
                else:
                    summoner_name = get_summoner_name(api_key, region, summoner_id) if summoner_id else 'Unknown'
                    name_cache[summoner_id] = summoner_name

                row = [
                    summoner_name,
                    rank,
                    entry.get('leaguePoints', 0),
                    entry.get('wins', 0),
                    entry.get('losses', 0)
                ]
                writer.writerow(row)

# Hauptprogramm
if __name__ == "__main__":
    API_KEY = "RGAPI-4014f792-fae2-4b89-9bdd-54e1aff63b96"  # Ersetze dies mit deinem API-Key
    REGION = "euw1"           # Beispiel: "na1", "euw1", "eun1", etc.

    # Daten für Challenger, Grandmaster und Master abrufen
    tiers = ["challenger", "grandmaster", "master"]
    data_list = []

    for tier in tiers:
        tft_league_data = get_tft_league_data(API_KEY, REGION, tier)
        if tft_league_data:
            data_list.append({
                'rank': tier.capitalize(),
                'entries': tft_league_data['entries']
            })

    if data_list:
        FILENAME = "tft_league_data.csv"
        save_to_csv(data_list, FILENAME, API_KEY, REGION)
        print(f"Daten erfolgreich in {FILENAME} gespeichert.")