import pandas as pd

def convert_to_dataframe(games):
    """
    Converts the games data into a pandas DataFrame for analysis.
    """
    return pd.DataFrame([{
        "AppID": game.get("appid", "N/A"),
        "Name": game.get("name", "N/A"),
        "Playtime (Hours)": round(game.get("playtime_forever", 0) / 60, 2),
        "Playtime (Minutes)": game.get("playtime_forever", 0)
    } for game in games])

def convert_stats_to_dataframe(stats_player1, stats_player2):
    """
    Converts the player stats into a comparison DataFrame.
    """
    stats_dict = {"Stat": [], "Player 1": [], "Player 2": []}
    for stat in stats_player1:
        stats_dict["Stat"].append(stat["name"])
        stats_dict["Player 1"].append(stat["value"])
        # Find the corresponding stat for Player 2
        stat_player2 = next((s for s in stats_player2 if s["name"] == stat["name"]), None)
        stats_dict["Player 2"].append(stat_player2["value"] if stat_player2 else "N/A")

    return pd.DataFrame(stats_dict)