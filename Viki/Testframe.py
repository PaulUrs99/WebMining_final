import pandas as pd

# Spiele, welche für ein Dashboard zur Verfügung stehen
games = [
    {"appid": 730, "name": "Counter-Strike 2"},
    {"appid": 240, "name": "Counter-Strike: Source"},
    {"appid": 1086940, "name": "Baldur's Gate 3"}
]

# Direktes Erstellen des DataFrames aus einer Liste von Dictionaries
array_games = pd.DataFrame([{"App-ID": game["appid"], "Name": game["name"]} for game in games])

# Ausgabe des Arrays
print(array_games)