import requests
import csv

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

def save_to_csv(data_list, filename):
    # CSV-Header definieren
    headers = ["Summoner Name", "Rank", "LP", "Wins", "Losses"]

    # Daten in die CSV schreiben
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for data in data_list:
            rank = data['rank']
            for entry in data['entries']:
                row = [
                    entry.get('summonerName', 'Unknown'),
                    rank,
                    entry.get('leaguePoints', 0),
                    entry.get('wins', 0),
                    entry.get('losses', 0)
                ]
                writer.writerow(row)

# Hauptprogramm
if __name__ == "__main__":
    API_KEY = "RGAPI-329a152e-b1c3-43d2-ae63-392eab5761d7"  # Ersetze dies mit deinem API-Key
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
        FILENAME = "TFT-League-V1.csv"
        save_to_csv(data_list, FILENAME)
        print(f"Daten erfolgreich in {FILENAME} gespeichert.")



# Challenger-Liste enthält nur die Top 200 Spieler in der Rangliste der TFT-Challenger Division pro Region
# Challenger: 200 Spieler (feste Grenze).
# Grandmaster: Variiert je nach Region, aber typischerweise einige Hundert Spieler.
# Master: Variiert stark, normalerweise die größte Gruppe unter den Top-Spielern.