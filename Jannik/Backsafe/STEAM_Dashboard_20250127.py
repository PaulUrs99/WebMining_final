# ------------------------------------------------------------------------------------------------------------
# Import benötigter Bibliotheken
import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import user_owned_games
import user_stats
import user_info
import user_game
import user_dataframe as df
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
# Streamlit App
st.title("Steam Dashboard")

# Tabs erstellen
tabs = st.tabs(["Profilstatistiken", "In-Game-Statistiken", "Community-Vergleich", "Freunde-Vergleich"])

# API Key (du kannst eine sichere Methode verwenden, um den Schlüssel zu speichern)
API_KEY = "DB15759E609C1E342536A6973593A57F"  # Ersetze mit deinem Steam Web API Key
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
# Spiele, welche für ein Dashboard zur Verfügung stehen
games = [
    # {"appid": 0, "name": "--- Bitte auswählen ---"},
    {"appid": 730, "name": "Counter-Strike 2"},
    {"appid": 648800, "name": "Raft"},
    {"appid": 221100, "name": "DayZ"},
    {"appid": 222880, "name": "Insurgency"}
]

# Direktes Erstellen des DataFrames aus einer Liste von Dictionaries
array_games = pd.DataFrame([{"App-ID": game["appid"], "Name": game["name"]} for game in games])

# Ausgabe des Arrays
# print(array_games)
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
STAT_MAPPING = {
    '730': [  # Counter-Strike 2 - ok 60-80 Mio monatlich // 76561198346540208, 76561198066213451 // Lucian: 76561198272436700, 76561198274285500, 76561198410958900, 76561197969869100, 76561198190556600
        "total_kills",
        "total_deaths",
        "total_time_played",
        "total_wins",
        "total_kills_headshot",
        "total_shots_hit",
        "total_shots_fired",
        "total_rounds_played",
        "total_matches_won",
        "total_matches_played",
        "total_gg_matches_won",
        "total_gg_matches_played"
    ],
    '648800': [  # Raft - 10-20 Mio // 76561198989615860, 76561199519041475 // Lucian: 76561199125748500, 76561198840295700, 76561198094944200, 76561198038187200, 76561198384517700
        "stat_player_deaths",
        "stat_player_sharkKills",
        "stat_player_birdKills",
        "stat_player_pufferKills",
        "stat_player_stoneBirdKills",
        "stat_player_ratKills",
        "stat_player_bearKills",
        "stat_player_botKills",
        "stat_player_anglerFishKills",
        "stat_player_boarKills",
        "stat_player_captures_bee",
        "stat_player_capturedAnimals",
        "stat_player_instrumentNotes_played",
        "stat_player_fireworks_launched",
        "stat_player_excevations_treasure",
        "stat_build_paintCount",
        "stat_build_removeCount",
        "stat_player_hookCount",
        "stat_build_foundationCount",
        "stat_player_zipline_distance",
        "stat_player_zipline_distanceOneGo",
        "stat_player_token_spend_tangaroa"
    ],
    '221100': [  # DayZ - ? 7,7-10,7 Mio // 76561198137195513, 76561198082372757 // Lucian: 76561198047709700, 76561198040157400, 76561198282747300, 76561198133690000, 76561198963095000
        "STAT_ACTION_EAT",
        "STAT_ACTION_DRINK",
        "STAT_ACTION_EQUIP_GEAR",
        "STAT_ACTION_COOK_STEAK",
        "STAT_ACTION_IGNITE_FIRE_MATCHBOX",
        "STAT_ACTION_IGNITE_FIRE_HAND_DRILL",
        "STAT_ACTION_SHAVE",
        "STAT_ACTION_GUT_DEER",
        "STAT_ACTION_APPLY_MEDS_ON_SURVIVOR",
        "STAT_INFECTED_KILL_COUNT",
        "STAT_SURVIVOR_KILL_MAX_DIST",
        "STAT_INFECTED_SOLDIER_KILL_COUNT",
        "STAT_SURVIVOR_MELEE_KILL_COUNT",
        "STAT_SURVIVOR_HEADSHOT_COUNT",
        "STAT_INFECTED_HEADSHOT_COUNT",
        "STAT_HEADSHOT_COUNT"
    ],
    '222880': [  # Insurgency - ok // 76561198034931808, 76561198853081788, 76561198088969488 // Lucian: 76561198418483600, 76561198019450600, 76561198027002400, 76561198204790000, 76561198052773000
       "TotalKills",
        "TotalCaptures",
        "TotalMVPs",
        "TotalHeroCaptures",
        "TotalKillsCoop",
        "TotalCapturesCoop",
        "TotalMVPsCoop",
        "TotalHeroCapturesCoop",
        "TotalKillsAll",
        "TotalCapturesAll",
        "TotalMVPsAll",
        "TotalHeroCapturesAll"
    ],
    # Weitere App-IDs
    # '440': [...],
}

# Dictionary zur Umbenennung von Keys in lesbare Namen
STAT_LABELS = {
    "total_kills": "Abschüsse insgesamt",
    "total_deaths": "Tode insgesamt",
    "total_time_played": "Zeit In-Game (Sek.)",
    "total_wins": "Siege insgesamt",
    "total_kills_headshot": "Headshots",
    "total_shots_hit": "Treffer",
    "total_shots_fired": "Abgefeuerte Schüsse",
    "total_rounds_played": "Gespielte Runden",
    "total_matches_won": "Gewonnene Matches",
    "total_matches_played": "Gespielte Matches",
    "total_gg_matches_won": "GunGame-Siege",
    "total_gg_matches_played": "GunGame-Spiele",
    "stat_player_deaths": "Anzahl der Tode",
    "stat_player_deaths": "Anzahl der Tode",
    "stat_player_sharkKills": "Anzahl der getöteten Haie",
    "stat_player_birdKills": "Anzahl der getöteten Vögel",
    "stat_player_pufferKills": "Anzahl der getöteten Kugelfische",
    "stat_player_stoneBirdKills": "Anzahl der getöteten Steinwurf-Vögel",
    "stat_player_ratKills": "Anzahl der getöteten Ratten",
    "stat_player_bearKills": "Anzahl der getöteten Bären",
    "stat_player_botKills": "Anzahl der getöteten Roboter",
    "stat_player_anglerFishKills": "Anzahl der getöteten Anglerfische",
    "stat_player_boarKills": "Anzahl der getöteten Wildschweine",
    "stat_player_captures_bee": "Anzahl der gesammelten Bienenschwärme",
    "stat_player_capturedAnimals": "Anzahl der eingefangenen Tiere",
    "stat_player_instrumentNotes_played": "Anzahl der gespielten Noten mit Musikinstrumenten",
    "stat_player_fireworks_launched": "Anzahl der abgefeuerten Feuerwerke",
    "stat_player_excevations_treasure": "Anzahl der ausgegrabenen Schätze",
    "stat_build_paintCount": "Anzahl der bemalten Objekte",
    "stat_build_removeCount": "Anzahl der entfernten Strukturen",
    "stat_player_hookCount": "Anzahl der Verwendungen des Hakens",
    "stat_build_foundationCount": "Anzahl der gebauten Fundamente",
    "stat_player_zipline_distance": "Zurückgelegte Distanz mit der Seilrutsche (gesamt)",
    "stat_player_zipline_distanceOneGo": "Maximale Distanz mit der Seilrutsche in einem Durchgang",
    "stat_player_token_spend_tangaroa": "Ausgegebene Tokens auf Tangaroa",
    "STAT_ACTION_EAT": "Anzahl der Aktionen, bei denen Nahrung gegessen wurde",
    "STAT_ACTION_DRINK": "Anzahl der Aktionen, bei denen Wasser oder andere Flüssigkeiten getrunken wurden",
    "STAT_ACTION_COOK_STEAK": "Anzahl der gekochten Steaks",
    "STAT_ACTION_IGNITE_FIRE_MATCHBOX": "Anzahl der entzündeten Feuer mit Streichhölzern",
    "STAT_ACTION_IGNITE_FIRE_HAND_DRILL": "Anzahl der entzündeten Feuer mit einem Handbohrer",
    "STAT_ACTION_EQUIP_GEAR": "Anzahl der Aktionen, bei denen Ausrüstung angelegt wurde",
    "STAT_ACTION_SHAVE": "Anzahl der durchgeführten Rasuren",
    "STAT_ACTION_GUT_DEER": "Anzahl der ausgeweideten Hirsche",
    "STAT_ACTION_APPLY_MEDS_ON_SURVIVOR": "Anzahl der Anwendungen von Medikamenten auf andere Überlebende",
    "STAT_INFECTED_KILL_COUNT": "Anzahl der getöteten Infizierten",
    "STAT_INFECTED_SOLDIER_KILL_COUNT": "Anzahl der getöteten infizierten Soldaten",
    "STAT_INFECTED_HEADSHOT_COUNT": "Anzahl der Kopfschüsse auf Infizierte",
    "STAT_SURVIVOR_KILL_MAX_DIST": "Maximale Distanz, aus der ein Überlebender getötet wurde",
    "STAT_SURVIVOR_MELEE_KILL_COUNT": "Anzahl der getöteten Überlebenden mit Nahkampfwaffen",
    "STAT_SURVIVOR_HEADSHOT_COUNT": "Anzahl der Kopfschüsse auf Überlebende",
    "STAT_HEADSHOT_COUNT": "Gesamtanzahl aller Kopfschüsse",
    "TotalKills": "Gesamtanzahl der Kills im kompetitiven Modus",
    "TotalCaptures": "Gesamtanzahl der eroberten Ziele im kompetitiven Modus",
    "TotalMVPs": "Gesamtanzahl der MVP-Auszeichnungen im kompetitiven Modus",
    "TotalHeroCaptures": "Gesamtanzahl der heldenhaften Eroberungen (entscheidende Eroberungen) im kompetitiven Modus",
    "TotalKillsCoop": "Gesamtanzahl der Kills im Koop-Modus",
    "TotalCapturesCoop": "Gesamtanzahl der eroberten Ziele im Koop-Modus",
    "TotalMVPsCoop": "Gesamtanzahl der MVP-Auszeichnungen im Koop-Modus",
    "TotalHeroCapturesCoop": "Gesamtanzahl der heldenhaften Eroberungen im Koop-Modus",
    "TotalKillsAll": "Gesamtanzahl der Kills in allen Modi",
    "TotalCapturesAll": "Gesamtanzahl der eroberten Ziele in allen Modi",
    "TotalMVPsAll": "Gesamtanzahl der MVP-Auszeichnungen in allen Modi",
    "TotalHeroCapturesAll": "Gesamtanzahl der heldenhaften Eroberungen in allen Modi"
}
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
# Tab "Deine Statistiken"
with tabs[0]:
    st.header("Profilstatistiken")
    st.subheader("Gib deine Steam-ID ein, um deine Profilstatistiken zu sehen und die weiteren Funktionen nutzen zu können:")

    # CSS für die vertikale Ausrichtung und zentrierten Text im Eingabefeld
    st.markdown(
        """
        <style>
        input {
            text-align: center; /* Zentriere den Text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    steam_id = st.text_input(label="STEAM-ID", placeholder="--- Gib hier Deine SteamID64 ein ---", label_visibility="hidden")
    
    if steam_id:  # Daten laden
        with st.spinner("Daten werden geladen..."):
            result = user_owned_games.get_owned_games(API_KEY, steam_id)
            info_result = user_info.get_user_info(API_KEY, steam_id)

        # Benutzerinformationen anzeigen
        if "error" in info_result:
            st.error(f"Fehler: {info_result['error']}")
        else:
            st.subheader("Benutzerinformationen")

            # Layout mit zwei Spalten
            col1, col2 = st.columns([3, 1])  # Verhältnis der Spaltenbreite: 1:3

            # Linke Spalte: Benutzerinfos
            with col1:
                st.write(f"**Benutzername:** {info_result['personaname']}")
                st.write(f"**Letzter Logoff:** {info_result['lastlogoff']}")
                st.write(f"**Konto erstellt am:** {info_result['timecreated']}")
                st.write(f"**Tage seit Kontoerstellung:** {info_result['days_since_creation']}")

            # Rechte Spalte: Avatar
            with col2:
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                        <img src="{info_result['avatarfull']}" alt="Avatar" style="width: 100px; border-radius: 0%;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # st.image(info_result['avatarfull'], width=100) # Ursprüngliche Positionierung
            
            days_since_creation = info_result['days_since_creation']

        if "error" in result:
            st.error(f"Fehler: {result['error']}")
        else:
            games = result.get("response", {}).get("games", [])

            if not games:
                st.warning("Das Profil scheint 'privat' zu sein.") # Davor: Keine Spiele gefunden.
            else:
                st.subheader("Spielinformationen")

                df_games = df.convert_to_dataframe(games)[["Name", "Playtime (Hours)"]]

                # Tabelle sortieren
                df_games = df_games.sort_values(by="Playtime (Hours)", ascending=False).reset_index(drop=True)
                df_games.reset_index(drop=True, inplace=True)

                # Anzahl der Spiele und Gesamtsumme der Spielzeit berechnen
                total_games = len(df_games)  # Anzahl der Spiele
                total_playtime_hours = df_games["Playtime (Hours)"].sum()  # Gesamtsumme der Spielzeit
                total_playtime_days = total_playtime_hours / 24  # Gesamtsumme der Spielzeit in Tagen
                total_playtime_minutes = total_playtime_hours * 60

                if days_since_creation > 0:  # Sicherstellen, dass keine Division durch Null erfolgt
                    avg_daily_playtime_hours = total_playtime_hours / days_since_creation
                    avg_daily_playtime_minutes = avg_daily_playtime_hours * 60
                    percentage_lifetime_playtime = (total_playtime_days / days_since_creation) * 100
                    # playtime_ratio = total_playtime_days / days_since_creation
                    # avg_playtime_per_week = playtime_ratio * 7
                else:
                    avg_daily_playtime_hours = 0
                    percentage_lifetime_playtime = 0
                    # playtime_ratio = 0
                    # avg_playtime_per_week = 0

                # Anzeige der Ergebnisse
                st.write(f"**Anzahl aller Spiele:** {total_games}")
                # st.write(f"**Gesamtsumme der Spielzeit [Stunden]:** {total_playtime_hours:.2f}")
                st.write(f"**Gesamtsumme der Spielzeit:** {int(total_playtime_hours)} Stunden und {int(total_playtime_minutes % 60)} Minuten")
                st.write(f"**Durchschnittliche tägliche Spielzeit:** {int(avg_daily_playtime_hours)} Stunden und {int(avg_daily_playtime_minutes % 60)} Minuten")
                st.write(f"**Gesamtsumme der Spielzeit [Tage]:** {total_playtime_days:.0f}")
                # st.write(f"**Durchschnittliche Spieltage pro Woche:** {avg_playtime_per_week:.2f}")
                st.write(f"**Prozentsatz der Lebenszeit mit Spielen:** {percentage_lifetime_playtime:.2f} %")

                # Überschrift über den Spalten
                st.subheader("Deine Spiele (sortiert nach Spielzeit)")

                # CSS für die Zentrierung
                st.markdown(
                    """
                    <style>
                    .centered-table {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100%;  /* Nimmt die gesamte Höhe der Spalte ein */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Layout mit zwei Spalten
                col3, col4 = st.columns(2)

                # "Deine Spiele" in der linken Spalte
                with col3:
                    # st.subheader("Deine Spiele (sortiert nach Spielzeit)")
                    # st.dataframe(df_games)

                    st.markdown('<div class="centered-table">', unsafe_allow_html=True)
                    st.dataframe(df_games)
                    st.markdown('</div>', unsafe_allow_html=True)

                # "Top 10 Spiele" in der rechten Spalte
                with col4:
                    # st.subheader("Grafische Darstellung")
                    top_10 = df_games.head(10)
                    fig = px.bar(
                        top_10,
                        x="Name",
                        y="Playtime (Hours)",
                        title="Top 10 Spiele nach Spielzeit",
                        labels={"Name": "Spiel", "Playtime (Hours)": "Spielzeit (Stunden)"},
                        text_auto=True
                    )

                    # Einbettung der Grafik in ein zentriertes div
                    st.markdown('<div class="centered-chart">', unsafe_allow_html=True)
                    st.plotly_chart(fig, use_container_width=False)  # `use_container_width=False` für exakte Breite
                    st.markdown('</div>', unsafe_allow_html=True)

                    # st.plotly_chart(fig)

# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
# Tab "In-Game-Daten"
with tabs[1]:
    st.header("In-Game-Statistiken")

    # Array aktualisieren
    user_game_ids = [game["appid"] for game in games]  # App-IDs der Nutzer-Spiele
    array_games_updated = pd.DataFrame(
        # [array_games.iloc[0]] +  # Behalte den ersten Eintrag bei
        [row for _, row in array_games.iterrows() if row["App-ID"] in user_game_ids]  # Füge nur vorhandene Spiele hinzu
    )

    # Dropdown-Menü mit dem aktualisierten Array
    st.subheader("Wähle ein Spiel aus der Liste für weitere Statistiken:")
    selected_game = st.selectbox(
        "",
        array_games_updated["Name"],
        key = "selectbox1"
    )

    # App-ID ermitteln
    chosen_app_id = array_games_updated.loc[
        array_games_updated["Name"] == selected_game, "App-ID"
    ].values[0]

    if steam_id != "":
        if st.button("In-Game-Daten abrufen"):
            # Hier rufst du jetzt deine Methode aus user_stats auf.
            st.write(f"**Rufe Daten für App-ID {chosen_app_id} ab...**")
            user_game_data = user_game.fetch_in_game_data(API_KEY, steam_id, chosen_app_id)

            if user_game_data["status"] == "success":
                # Liste mit Statistik-Dict kommt zurück
                stats_list = user_game_data["stats"]

                # Ermitteln, ob wir für die gewählte App-ID bestimmte Statistiken darstellen wollen
                relevant_stats = STAT_MAPPING.get(str(chosen_app_id), [])

                # Nur die Einträge aus stats_list filtern, die in 'relevant_stats' vorkommen
                filtered_stats = [stat for stat in stats_list if stat["name"] in relevant_stats]

                if len(filtered_stats) > 0:
                    # Tabelle ausgeben
                    # df_stats = pd.DataFrame(filtered_stats)
                    # st.write("**Relevante Statistiken**")
                    # st.dataframe(df_stats)
                    
                    # Dictionary aus den gefilterten Statistiken, um besser darauf zugreifen zu können 
                    stats_dict = {stat["name"]: stat["value"] for stat in filtered_stats}

                    # Key-Value-Format ausgeben
                    st.write("**Statistiken**")
                    
                    # Gib die Statistiken in der Reihenfolge aus, in der sie in STAT_MAPPING definiert sind
                    for stat_key in relevant_stats:
                        if stat_key in stats_dict:
                            value = stats_dict[stat_key]
                            display_name = STAT_LABELS.get(stat_key, stat_key)
                            
                            st.write(f"{display_name}: {value:.0f}".replace(',', '.'))

                            # Darstellung für Counter-Strike 2
                            if chosen_app_id == 730:

                                # Tod-Abschuss-Ratio
                                if stat_key == "total_deaths":
                                    deaths = stats_dict[stat_key]
                                    kills = stats_dict.get("total_kills", 0)
                                    if deaths > 0:
                                        death_ratio = kills / deaths
                                    else:
                                        death_ratio = "∞"  # Vermeidung Division durch Null (String-Wert-Rückgabe -> deswegen if-Bedinung in Ausgabe!)

                                    st.write(f"Tod-Abschuss-Ratio: 1 : {death_ratio:.2f}" if isinstance(death_ratio, float) else f"Kill-Abschuss-Ratio: 1:{death_ratio}")

                                # Trefferquote direkt nach "Abgefeuerte Schüsse" ausgeben + Kreisdiagramm
                                if stat_key == "total_shots_fired":
                                    shots_fired = stats_dict[stat_key]
                                    shots_hit   = stats_dict.get("total_shots_hit", 0)
                                    headshots = stats_dict.get("total_kills_headshot", 0)
                                    shots_missed = shots_fired - shots_hit  # Verfehlte Schüsse direkt berechnen

                                    if shots_fired > 0:
                                        accuracy = shots_hit / shots_fired * 100
                                        headshot_ratio = headshots / shots_hit * 100 if shots_hit > 0 else 0
                                        st.write(f"Trefferquote: {accuracy:.1f} %")
                                        st.write(f"Headshotquote: {headshot_ratio:.1f} %")

                                        # Kreisdiagramm erstellen
                                        labels = ["Treffer", "Verfehlt"]
                                        sizes = [shots_hit, shots_missed]
                                        colors = ["#4CAF50", "#FFC107"]
                                        explode = (0.1, 0)  # Nur das erste Segment hervorheben

                                        fig, ax = plt.subplots()
                                        ax.pie(
                                            sizes,
                                            explode=explode,
                                            labels=labels,
                                            colors=colors,
                                            autopct=lambda p: f'{p:.1f}%\n{int(sizes[int(p > 50)]):,.0f}'.replace(',', '.'),
                                            startangle=140,
                                        )
                                        ax.axis("equal")  # Gleichmäßige Darstellung des Kreises
                                        st.pyplot(fig)

                                        # Zusätzlicher Hinweis auf Headshots
                                        fig2, ax2 = plt.subplots()
                                        headshot_labels = ["Headshots", "Andere Treffer"]
                                        headshot_sizes = [headshots, shots_hit - headshots]
                                        headshot_colors = ["#2196F3", "#8BC34A"]
                                        explode_headshots = (0.1, 0)

                                        ax2.pie(
                                            headshot_sizes,
                                            explode=explode_headshots,
                                            labels=headshot_labels,
                                            colors=headshot_colors,
                                            autopct=lambda p: f'{p:.1f}%\n{int(headshot_sizes[int(p > 50)]):,.0f}'.replace(',', '.'),
                                            startangle=140,
                                        )
                                        ax2.axis("equal")
                                        st.pyplot(fig2)
                                
                                # Siegesquote direkt nach "Gespielte Matches" ausgeben
                                if stat_key == "total_matches_played":
                                    matches_played = stats_dict[stat_key]
                                    matches_won    = stats_dict.get("total_matches_won", 0)
                                    if matches_played > 0:
                                        win_ratio = matches_won / matches_played * 100
                                        st.write(f"Siegesquote: {win_ratio:.1f} %")

                    # for stat_dict in filtered_stats:
                    #     # st.write(f"{stat_dict['name']}: {stat_dict['value']}")
                    
                    #     original_name = stat_dict['name']         # z.B. "total_kills"
                    #     stat_value    = stat_dict['value']
                        
                    #     # Hole den sprechenden Namen aus STAT_LABELS oder nutze notfalls den Originalnamen
                    #     display_name = STAT_LABELS.get(original_name, original_name)
                        
                    #     st.write(f"{display_name}: {stat_value}")
                else:
                    st.warning("Für diese App-ID sind entweder keine relevanten Statistiken definiert oder es liegen keine Daten vor.")
                
                # # Als Tabelle (DataFrame) ausgeben
                # df_stats = pd.DataFrame(stats_list)
                # st.dataframe(df_stats)
                
            else:
                # Fehler anzeigen
                st.error(user_game_data.get("message", "Unbekannter Fehler"))
    else:
        st.warning("Es wurde noch keine Steam-ID angegeben!")

# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------

# Tab "Freunde Vergleich"
with tabs[2]:
    st.header("Community-Vergleich")

    # Dropdown-Menü mit dem aktualisierten Array
    st.subheader("Wähle ein Spiel aus der Liste für weitere Statistiken:")
    selected_game = st.selectbox(
        "",
        array_games_updated["Name"],
        key = "selectbox2"
    )

    # App-ID ermitteln
    chosen_app_id = array_games_updated.loc[
        array_games_updated["Name"] == selected_game, "App-ID"
    ].values[0]

    # if steam_id != "":
    #     # Weiter im Code
    # else:
    #     st.warning("Es wurde noch keine Steam-ID angegeben!")
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
# Tab "Freunde Vergleich"
with tabs[3]:
    st.header("Freunde-Vergleich")

    steam_id_1 = st.text_input(label="STEAM-ID", placeholder="--- Gib hier die erste SteamID64 ein ---", label_visibility="hidden")
    steam_id_2 = st.text_input(label="STEAM-ID", placeholder="--- Gib hier die zweite SteamID64 ein ---", label_visibility="hidden")
    button_compare = st.button("Vergleichen")

    if steam_id_1 and steam_id_2:
        st.write(f"Vergleich von Steam-IDs: {steam_id_1} und {steam_id_2}")
        st.write("Spiele werden geladen...")

        result_1 = user_owned_games.get_owned_games(API_KEY, steam_id_1)
        result_2 = user_owned_games.get_owned_games(API_KEY, steam_id_2)

        if "error" in result_1:
            st.error(f"Fehler bei der ersten SteamID: {result_1['error']}")
        elif "error" in result_2:
            st.error(f"Fehler bei der zweiten SteamID: {result_2['error']}")
        else:
            games_1 = result_1.get("response", {}).get("games", [])
            games_2 = result_2.get("response", {}).get("games", [])

            if not games_1:
                st.warning("Keine Spiele für die erste SteamID gefunden.")
            elif not games_2:
                st.warning("Keine Spiele für die zweite SteamID gefunden.")
            else:
                df_1 = df.convert_to_dataframe(games_1)[["Name", "Playtime (Hours)"]]
                df_2 = df.convert_to_dataframe(games_2)[["Name", "Playtime (Hours)"]]

                # Store app ids and names in a separate list
                app_ids_1 = {game.get("name", f"Unbekannt_{game.get('appid', 'N/A')}"): game.get("appid") for game in games_1}
                app_ids_2 = {game.get("name", f"Unbekannt_{game.get('appid', 'N/A')}"): game.get("appid") for game in games_2}

                common_games = pd.merge(df_1, df_2, on="Name", suffixes=('_Player1', '_Player2'))

                st.subheader("Gemeinsame Spiele")
                if not common_games.empty:
                    st.dataframe(common_games)

                    selected_game = st.selectbox("Wähle ein Spiel für weitere Statistiken:", common_games["Name"])

                    if selected_game:
                        app_id = app_ids_1[selected_game]

                        stats_player1 = user_stats.get_user_stats_for_game(API_KEY, steam_id_1, app_id)
                        stats_player2 = user_stats.get_user_stats_for_game(API_KEY, steam_id_2, app_id)

                        st.subheader(f"Statistiken für {selected_game} - Spieler 1")
                        st.json(stats_player1 if isinstance(stats_player1, list) else stats_player1.get("error", "Keine Daten gefunden."))

                        st.subheader(f"Statistiken für {selected_game} - Spieler 2")
                        st.json(stats_player2 if isinstance(stats_player2, list) else stats_player2.get("error", "Keine Daten gefunden."))
                else:
                    st.write("Keine gemeinsamen Spiele gefunden.")
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
    #76561198990374557 - paul.u1111
    #76561198254607847 - ImRizzex
    #76561198080617859 - ConCHEATER Wurst (Leopold Stotch)
    #76561197979048211 - floblak3
    #76561198364896644 - Yoink (Nathan)
    #76561198059410849 - jdvmb (viki)
    #76561198286398265 - theo_o (Daniel)
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
