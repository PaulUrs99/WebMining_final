import requests
import csv
from datetime import datetime

# Riot Games API URL
API_URL = "https://euw1.api.riotgames.com/lol/clash/v1/tournaments"
API_KEY = "RGAPI-329a152e-b1c3-43d2-ae63-392eab5761d7"  # Ersetze dies mit deinem eigenen API-Schlüssel

# Funktion zum Abrufen der Turnierdaten
def fetch_clash_data():
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler: {response.status_code} - {response.text}")
        return []

# Daten in einer CSV speichern
def save_to_csv(data):
    filename = f"CLASH-V1_{datetime.now().strftime('%Y-%m-%d')}.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Header für die CSV
        writer.writerow(["Tournament ID", "Theme ID", "Name Key", "Name Key Secondary", "Schedule"])
        
        # Daten schreiben
        for tournament in data:
            schedule = "; ".join([str(event) for event in tournament.get("schedule", [])])
            writer.writerow([
                tournament.get("id"),
                tournament.get("themeId"),
                tournament.get("nameKey"),
                tournament.get("nameKeySecondary"),
                schedule
            ])
    
    print(f"Daten gespeichert in {filename}")

# Hauptprogramm
if __name__ == "__main__":
    clash_data = fetch_clash_data()
    if clash_data:
        save_to_csv(clash_data)
