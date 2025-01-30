import requests
import csv

# Riot API Key hier einfügen
API_KEY = "RGAPI-329a152e-b1c3-43d2-ae63-392eab5761d7"
REGION = "euw1"  # Beispiel: EUW für Europa
SUMMONER_NAME = "floblak3"  # Name des Spielers, dessen Daten du abrufen möchtest

def get_summoner_id(summoner_name):
    """Holt die Summoner-ID eines Spielers."""
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Fehler beim Abrufen der Summoner-ID: {response.status_code}")
        return None

def get_champion_mastery(summoner_id):
    """Holt Champion-Mastery-Daten für einen Spieler."""
    url = f"https://{REGION}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler beim Abrufen der Champion-Mastery-Daten: {response.status_code}")
        return None

def save_to_csv(data, filename):
    """Speichert die Daten in einer CSV-Datei."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Daten erfolgreich in {filename} gespeichert.")

def main():
    summoner_id = get_summoner_id(SUMMONER_NAME)
    if not summoner_id:
        return
    
    mastery_data = get_champion_mastery(summoner_id)
    if not mastery_data:
        return
    
    # Daten in eine CSV-Datei speichern
    save_to_csv(mastery_data, "CHAMPION-MASTERY-V4.csv")

if __name__ == "__main__":
    main()