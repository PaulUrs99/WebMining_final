import requests
import csv

def get_owned_games(api_key, steam_id, include_appinfo=True, include_played_free_games=False):
    """
    Fetches the owned games of a Steam user using the Steam Web API.

    :param api_key: Your Steam Web API key (string).
    :param steam_id: The SteamID64 of the user (string).
    :param include_appinfo: Whether to include app info (default: True).
    :param include_played_free_games: Whether to include free games (default: False).
    :return: JSON response with the list of owned games or an error message.
    """
    base_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"

    params = {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": str(include_appinfo).lower(),  # Convert boolean to 'true' or 'false'
        "include_played_free_games": str(include_played_free_games).lower(),
        "format": "json"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
def save_to_csv(data, filename="STEAM_FLO.csv"):
    """
    Saves the owned games data to a CSV file.

    :param data: List of games data from the API response.
    :param filename: Name of the CSV file (default: 'owned_games.csv').
    """
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(["AppID", "Name", "Playtime (Hours)"])

            # Write the game data
            for game in data:
                appid = game.get("appid", "N/A")
                name = game.get("name", "N/A")
                playtime_hours = game.get("playtime_forever", 0) / 60  # Convert minutes to hours
                writer.writerow([appid, name, round(playtime_hours, 2)])

        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    # Replace these values with your actual API key and SteamID64
    API_KEY = "F06E65C071B7ABDE4CE3B531A06123E2"  # Replace with your Steam Web API key
    STEAM_ID = "76561197979048211"  # Replace with the SteamID64 of the user

    # Call the function to fetch owned games
    result = get_owned_games(API_KEY, STEAM_ID)

    # Check if the result contains an error
    if "error" in result:
        print("Error:", result["error"])
    else:
        games = result.get("response", {}).get("games", [])
        if games:
            print(f"Found {len(games)} games. Saving to CSV...")
            save_to_csv(games)
        else:
            print("No games found for the specified user.")
