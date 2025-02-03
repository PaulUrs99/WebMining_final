import requests
import json
import os
import csv

# Methode zur Speicherung des Fortschritts
INDEX_FILE = "progress_index.txt"

def save_progress(index, steam_id):
    with open(INDEX_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Index", "SteamID"])
        writer.writerow([index, steam_id])

def load_progress():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                return int(row["Index"]), row["SteamID"]
    return 0, None

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
        if 'playerstats' in data:
            return data['playerstats']
        else:
            return {"error": "Keine Statistiken gefunden oder Profil ist privat."}
    else:
        return {"error": f"Fehler beim Abrufen der Daten. Statuscode: {response.status_code}"}

if __name__ == "__main__":
    
    API_KEY = "DB15759E609C1E342536A6973593A57F"

    # Ordner erstellen, falls nicht vorhanden
    OUTPUT_DIR = r"C:\Users\paulu\OneDrive\Dokumente\GitHub\WebMining\Paul\Spielerdaten"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Fortschritt laden
    start_index, last_steam_id = load_progress()

   # CSV-Datei einlesen
    csv_file_path = "C:\\Users\\paulu\\OneDrive\\Dokumente\\GitHub\\WebMining\\fltered_data.csv"
    with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    # Iteration über die CSV-Daten
    for index, row in enumerate(rows[start_index:], start=start_index):
        steam_id = row["steam_64_id"]
        app_id = row["appid"]
        spielname = row["name"]  # Spaltenname muss in der CSV existieren

        output_file = os.path.join(OUTPUT_DIR, f"{spielname}_{steam_id}.json")

        # Überprüfen, ob die Datei bereits existiert
        if os.path.exists(output_file):
            print(f"Überspringe {output_file}, da es bereits existiert.")
            continue

        print(f"Bearbeite Index {index}: Spielname: {spielname}, SteamID: {steam_id}, AppID: {app_id}")

        # Daten abrufen
        player_data = get_owned_games(API_KEY, steam_id, app_id)

        # Fehler abfangen und überspringen, wenn Statuscode 403 auftritt
        if "error" in player_data and "Statuscode: 403" in player_data["error"]:
            print(f"Fehler 403 bei SteamID {steam_id}, überspringe diesen Datensatz.")
            save_progress(index + 1, steam_id)
            continue

        # Speichern der Daten in einer JSON-Datei
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(player_data, json_file, ensure_ascii=False, indent=4)

        # Fortschritt speichern
        save_progress(index + 1, steam_id)

    print("Skript abgeschlossen.")

