import requests
import pandas as pd
import streamlit as st

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
    Converts the games data into a pandas DataFrame for analysis.
    """
    return pd.DataFrame([
        {
            "AppID": game.get("appid", "N/A"),
            "Name": game.get("name", "N/A"),
            "Playtime (Hours)": round(game.get("playtime_forever", 0) / 60, 2)
        }
        for game in games
    ])

# Streamlit App
st.title("Steam Owned Games Comparison Dashboard")

# API Key (you might replace this with a secure method of fetching the key)
API_KEY = "F06E65C071B7ABDE4CE3B531A06123E2"  # Replace with your Steam Web API key

# User input for SteamIDs
steam_id_1 = st.text_input("Gib die erste SteamID64 ein:", "")
steam_id_2 = st.text_input("Gib die zweite SteamID64 ein:", "")

if steam_id_1 and steam_id_2:
    st.write(f"Vergleich von Steam-IDs: {steam_id_1} und {steam_id_2}")
    st.write("Spiele werden geladen...")

    # Fetch games for both SteamIDs
    result_1 = get_owned_games(API_KEY, steam_id_1)
    result_2 = get_owned_games(API_KEY, steam_id_2)

    if "error" in result_1:
        st.error(f"Fehler bei der ersten SteamID: {result_1['error']}")
    elif "error" in result_2:
        st.error(f"Fehler bei der zweiten SteamID: {result_2['error']}")
    else:
        # Extract games data
        games_1 = result_1.get("response", {}).get("games", [])
        games_2 = result_2.get("response", {}).get("games", [])

        if not games_1:
            st.warning("Keine Spiele für die erste SteamID gefunden.")
        elif not games_2:
            st.warning("Keine Spiele für die zweite SteamID gefunden.")
        else:
            # Convert games data to DataFrames
            df_1 = convert_to_dataframe(games_1)
            df_2 = convert_to_dataframe(games_2)

            # Find common games
            common_games = pd.merge(df_1, df_2, on="Name", suffixes=("_Player1", "_Player2"))

            # Show DataFrames
            st.subheader("Spieler 1 - Liste der Spiele")
            st.dataframe(df_1)

            st.subheader("Spieler 2 - Liste der Spiele")
            st.dataframe(df_2)

            st.subheader("Gemeinsame Spiele")
            if not common_games.empty:
                st.dataframe(common_games)
            else:
                st.write("Keine gemeinsamen Spiele gefunden.")

            # Top 5 played games for each player
            top_5_player1 = df_1.sort_values(by="Playtime (Hours)", ascending=False).head(5)
            top_5_player2 = df_2.sort_values(by="Playtime (Hours)", ascending=False).head(5)

            st.subheader("Top 5 gespielte Spiele - Spieler 1")
            st.dataframe(top_5_player1)

            st.subheader("Top 5 gespielte Spiele - Spieler 2")
            st.dataframe(top_5_player2)