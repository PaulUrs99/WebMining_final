import requests
import csv
import streamlit as st
import pandas as pd

def get_owned_games(api_key, steam_id, include_appinfo=True, include_played_free_games=False):
    """
    Fetches the owned games of a Steam user using the Steam Web API.
    """
    base_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": str(include_appinfo).lower(),
        "include_played_free_games": str(include_played_free_games).lower(),
        "format": "json"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def convert_to_dataframe(games):
    """
    Converts the games data into a pandas DataFrame for display in Streamlit.
    """
    game_data = [
        {
            "AppID": game.get("appid", "N/A"),
            "Name": game.get("name", "N/A"),
            "Playtime (Hours)": round(game.get("playtime_forever", 0) / 60, 2)
        }
        for game in games
    ]
    return pd.DataFrame(game_data)

# Streamlit App
st.title("Steam Owned Games Dashboard")

# API Key (you might replace this with a secure method of fetching the key)
API_KEY = "F06E65C071B7ABDE4CE3B531A06123E2"  # Replace with your Steam Web API key

# User input for SteamID
steam_id = st.text_input("Gib deine SteamID64 ein:", "")

if steam_id:
    st.write(f"SteamID: {steam_id}")
    st.write("Spiele werden geladen...")

    # Fetch games using the API
    result = get_owned_games(API_KEY, steam_id)

    if "error" in result:
        st.error(f"Fehler beim Abrufen der Daten: {result['error']}")
    else:
        games = result.get("response", {}).get("games", [])
        if games:
            st.success(f"{len(games)} Spiele gefunden!")
            
            # Convert to DataFrame and display
            games_df = convert_to_dataframe(games)
            st.dataframe(games_df)

            # Option to download as CSV
            csv = games_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Spiele als CSV herunterladen",
                data=csv,
                file_name="owned_games.csv",
                mime="text/csv",
            )
        else:
            st.warning("Keine Spiele für den angegebenen Nutzer gefunden.")