import requests
import csv

# Deine Riot API-Schlüssel hier einfügen
API_KEY = "RGAPI-329a152e-b1c3-43d2-ae63-392eab5761d7"
BASE_URL = "https://euw1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I"

def fetch_data_from_api():
    """
    Ruft Daten aus der Riot API ab.
    """
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(BASE_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler bei der Anfrage: {response.status_code} - {response.text}")
        return None

def save_to_csv(data, filename):
    """
    Speichert die Daten in einer CSV-Datei.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # CSV-Header
        writer.writerow(["Summoner Name", "Tier", "Rank", "LP", "Wins", "Losses", "Queue Type"])
        
        for entry in data:
            writer.writerow([
                entry.get("summonerName"),
                entry.get("tier"),
                entry.get("rank"),
                entry.get("leaguePoints"),
                entry.get("wins"),
                entry.get("losses"),
                entry.get("queueType")
            ])
    print(f"Daten gespeichert in: {filename}")

def main():
    data = fetch_data_from_api()
    if data:
        save_to_csv(data, "lLeague-Exp-V4.csv")

if __name__ == "__main__":
    main()