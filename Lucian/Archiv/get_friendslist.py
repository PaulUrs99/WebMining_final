import pandas as pd
import requests

# Datei mit den Steam-IDs und Ausgabe-Datei definieren
input_file = 'steam_ids_64.csv'
output_file = 'steam_friends.csv'
processed_file = 'processed_ids.csv'

# Steam Web API-Keys
api_keys = ['F06E65C071B7ABDE4CE3B531A06123E2', 'DB15759E609C1E342536A6973593A57F']
current_key_index = 0

# Basis-URL für die Abfrage der Freundesliste
base_url = "http://api.steampowered.com/ISteamUser/GetFriendList/v1/"

# Funktion zum Abrufen der Freundesliste
def get_friend_list(api_keys, steam_id):
    global current_key_index  # Macht die Variable global

    params = {
        "key": api_keys[current_key_index],
        "steamid": steam_id,
        "relationship": "friend"
    }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 429:  # API-Limit erreicht
            print(f"API-Key {api_keys[current_key_index]} hat das Limit erreicht.")
            current_key_index += 1
            if current_key_index >= len(api_keys):
                raise Exception("Alle API-Keys haben das Limit erreicht.")
            return get_friend_list(api_keys, steam_id)  # Erneut mit neuem API-Key versuchen
        response.raise_for_status()
        data = response.json()
        return data.get('friendslist', {}).get('friends', [])
    except Exception as e:
        print(f"Fehler bei der Abfrage für Steam-ID {steam_id}: {e}")
        return []

# Hauptskript
def main():
    steam_ids_df = pd.read_csv(input_file)
    if 'steam_64_id' not in steam_ids_df.columns:
        print("Die Eingabedatei muss eine Spalte namens 'steam_64_id' enthalten.")
        return

    try:
        existing_data = pd.read_csv(output_file)
    except FileNotFoundError:
        existing_data = pd.DataFrame(columns=['steam_id', 'friend_id'])

    try:
        processed_ids = pd.read_csv(processed_file)['steam_64_id'].tolist()
    except FileNotFoundError:
        processed_ids = []

    known_ids = set(steam_ids_df['steam_64_id']).union(processed_ids)
    print(f"Bereits bekannte IDs: {len(known_ids)}")

    results = []
    newly_processed_ids = []

    for steam_id in steam_ids_df['steam_64_id']:
        if steam_id in processed_ids:
            print(f"Steam-ID {steam_id} wurde bereits verarbeitet. Überspringe...")
            continue

        print(f"Abfrage der Freundesliste für Steam-ID: {steam_id}")
        friends = get_friend_list(api_keys, steam_id)

        if friends == []:
            print("Abbruch. Keine weiteren Freundeslisten können abgerufen werden.")
            continue

        for friend in friends:
            if friend['steamid'] not in known_ids:
                results.append({"steam_id": steam_id, "friend_id": friend['steamid']})
                known_ids.add(friend['steamid'])

        newly_processed_ids.append(steam_id)

        if len(results) > 0:
            results_df = pd.DataFrame(results)
            results_df.to_csv(output_file, mode='a', header=not existing_data.shape[0], index=False)
            print(f"{len(results)} Freundschaften gespeichert.")
            results = []

        processed_ids_df = pd.DataFrame({'steam_64_id': newly_processed_ids})
        processed_ids_df.to_csv(processed_file, mode='w', header=True, index=False)

    print("Skript abgeschlossen.")

if __name__ == "__main__":
    main()
