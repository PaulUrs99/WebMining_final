import requests
import csv

# Riot Games API-Schlüssel (ersetzen durch deinen eigenen API-Schlüssel)
API_KEY = 'RGAPI-329a152e-b1c3-43d2-ae63-392eab5761d7'
BASE_URL = 'https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations'

# Funktion, um Daten von der API zu holen
def fetch_champion_rotations():
    headers = {'X-Riot-Token': API_KEY}
    response = requests.get(BASE_URL, headers=headers)

    # Überprüfen, ob der Request erfolgreich war
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler: {response.status_code} - {response.text}")
        return None

# Daten speichern
def save_to_csv(data, filename='CHAMPION-ROTATIONS.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Header
        writer.writerow(['freeChampionIds', 'freeChampionIdsForNewPlayers', 'maxNewPlayerLevel'])

        # Daten
        writer.writerow([
            ', '.join(map(str, data['freeChampionIds'])),
            ', '.join(map(str, data['freeChampionIdsForNewPlayers'])),
            data['maxNewPlayerLevel']
        ])

# Hauptprogramm
if __name__ == '__main__':
    champion_data = fetch_champion_rotations()
    if champion_data:
        save_to_csv(champion_data)
        print("Daten erfolgreich gespeichert in 'champion_rotations.csv'")