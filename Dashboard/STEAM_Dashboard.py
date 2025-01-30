# ------------------------------------------------------------------------------------------------------------
# Import benötigter Bibliotheken
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import sys
sys.path.append(r"C:\Users\paulu\OneDrive\Dokumente\GitHub\WebMining\Dashboard\Hilfsfunktionen")
import user_owned_games
import user_stats
import user_info
import user_game
import user_dataframe as df

# ------------------------------------------------------------------------------------------------------------
def creds_entered():
    if st.session_state["user"].strip() == "admin" and st.session_state["pw"].strip() == "admin":
        st.session_state["authenticated"] = True
    else: 
        st.session_state["authenticated"] = False
        if not st.session_state["pw"]:
            st.warning("Bitte Passwort eingeben")
        elif not st.session_state["user"]:
            st.warning("Bitte Nutzernamen eingeben")
        else:
            st.error("Falsche Anmeldedaten")

def authenticate_user():
    if "authenticated" not in st.session_state:
        st.text_input(label="Username", key="user")
        st.text_input(label="Passwort", key="pw", type="password", on_change=creds_entered)
        return False
    else:
        if st.session_state["authenticated"]:
            return True
        else:
            st.text_input(label="Username", key="user")
            st.text_input(label="Passwort", key="pw", type="password", on_change=creds_entered)

if authenticate_user():
    # Hier wird das Dashboard bei erfolgreicher Authentifizierung geladen

# ------------------------------------------------------------------------------------------------------------
    # Streamlit App
    st.title("Steam Dashboard")

    # Tabs erstellen
    tabs = st.tabs(["Anmeldung", "Deine Statistiken", "Vergleich"])

    # API Key (du kannst eine sichere Methode verwenden, um den Schlüssel zu speichern)
    API_KEY = "DB15759E609C1E342536A6973593A57F" 
    # ------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------
    # Spiele, welche für ein Dashboard zur Verfügung stehen
    games = [
        {"appid": 0, "name": "--- Bitte auswählen ---"},
        {"appid": 730, "name": "Counter-Strike 2"},
        {"appid": 240, "name": "Counter-Strike: Source"},
        {"appid": 648800, "name": "Raft"},
        {"appid": 252490, "name": "Rust"},
        {"appid": 221100, "name": "DayZ"},
        {"appid": 218620, "name": "Payday2"},
        {"appid": 222880, "name": "Insurgency"},

    ]

    # Direktes Erstellen des DataFrames aus einer Liste von Dictionaries
    array_games = pd.DataFrame([{"App-ID": game["appid"], "Name": game["name"]} for game in games])

    # Ausgabe des Arrays
    # print(array_games)
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    with tabs[0]:
        "willkommen"

    # Tab "Deine Statistiken"
    with tabs[1]:
        st.header("Deine Statistiken")

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

        steam_id = st.text_input("", placeholder="--- Gib hier Deine SteamID64 ein ---")
        
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

                    # Array aktualisieren
                    user_game_ids = [game["appid"] for game in games]  # App-IDs der Nutzer-Spiele
                    array_games_updated = pd.DataFrame(
                        [array_games.iloc[0]] +  # Behalte den ersten Eintrag bei
                        [row for _, row in array_games.iterrows() if row["App-ID"] in user_game_ids]  # Füge nur vorhandene Spiele hinzu
                    )

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

                    # Dropdown-Menü mit dem aktualisierten Array
                    st.subheader("Wähle ein Spiel aus der Liste für weitere Statistiken:")
                    selected_game = st.selectbox(
                        "",
                        array_games_updated["Name"]
                    )

                    # App-ID ermitteln
                    if selected_game != "--- Bitte auswählen ---":
                        chosen_app_id = array_games_updated.loc[
                            array_games_updated["Name"] == selected_game, "App-ID"
                        ].values[0]

                        if st.button("In-Game-Daten abrufen"):
                            # Hier rufst du jetzt deine Methode aus user_stats auf.
                            st.write(f"**Rufe Daten für App-ID {chosen_app_id} ab...**")
                            user_game_data = user_game.fetch_in_game_data(API_KEY, steam_id, chosen_app_id)

                            if user_game_data["status"] == "success":
                                # Liste mit Statistik-Dict kommt zurück
                                stats_list = user_game_data["stats"]
                                
                                # Als Tabelle (DataFrame) ausgeben
                                df_stats = pd.DataFrame(stats_list)
                                st.dataframe(df_stats)
                                
                            else:
                                # Fehler anzeigen
                                st.error(user_game_data.get("message", "Unbekannter Fehler"))
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    # Tab "Vergleich"
    with tabs[2]:
        st.header("Vergleich")

        steam_id_1 = st.text_input("Gib die erste SteamID64 ein:", "")
        steam_id_2 = st.text_input("Gib die zweite SteamID64 ein:", "")
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