# Tab "In-Game-Daten"
with tabs[1]:
    st.header("In-Game-Statistiken")

    # Array aktualisieren
    user_game_ids = [game["appid"] for game in games]  # App-IDs der Nutzer-Spiele
    array_games_updated = pd.DataFrame(
        [row for _, row in array_games.iterrows() if row["App-ID"] in user_game_ids]  # Füge nur vorhandene Spiele hinzu
    )

    # **Fehlerhandling: Falls kein Spiel übrig ist oder 'Name' fehlt**
    if array_games_updated.empty or "Name" not in array_games_updated.columns:
        st.warning("Es wurde keine Übereinstimmung zwischen den Spielen des/der User/in und unseren Dashboard-Anzeigen gefunden.")
    else:
        # Dropdown-Menü mit dem aktualisierten Array
        st.subheader("Wähle ein Spiel aus der Liste für weitere Statistiken:")
        
        # 💡 Sicherstellen, dass "Name" existiert und als Liste übergeben wird
        selected_game = st.selectbox(
            "",
            array_games_updated["Name"].tolist(),  # Nutzt `.tolist()`, um Fehler zu vermeiden
            key="selectbox1"
        )

        # App-ID ermitteln (nur falls `selected_game` existiert)
        chosen_app_id = array_games_updated.loc[
            array_games_updated["Name"] == selected_game, "App-ID"
        ].values[0]

        if steam_id != "":
            if st.button("In-Game-Daten abrufen"):
                # Hier rufst du jetzt deine Methode aus user_stats auf.
                st.write(f"**Rufe Daten für App-ID {chosen_app_id} ab...**")
                user_game_data = user_game.fetch_in_game_data(API_KEY, steam_id, chosen_app_id)

                if user_game_data.get("status") == "success":
                    # Liste mit Statistik-Dict kommt zurück
                    stats_list = user_game_data.get("stats", [])

                    # Ermitteln, ob wir für die gewählte App-ID bestimmte Statistiken darstellen wollen
                    relevant_stats = STAT_MAPPING.get(str(chosen_app_id), [])

                    # Nur die Einträge aus stats_list filtern, die in 'relevant_stats' vorkommen
                    filtered_stats = [stat for stat in stats_list if stat["name"] in relevant_stats]
# -----
                    if len(filtered_stats) > 0 and chosen_app_id == 730:
                        # Tabelle ausgeben
                        # df_stats = pd.DataFrame(filtered_stats)
                        # st.write("**Relevante Statistiken**")
                        # st.dataframe(df_stats)
                        
                        # Dictionary aus den gefilterten Statistiken, um besser darauf zugreifen zu können 
                        stats_dict = {stat["name"]: stat["value"] for stat in filtered_stats}

                        # Key-Value-Format ausgeben
                        st.write("**Statistiken**")

                        def custom_metric(label, value):
                            st.markdown(
                                f"""
                                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                                    <div style="text-align: left; width: 100%; font-size: 16px; font-weight: normal; color: #6c757d;">{label}</div>
                                    <div style="font-size: 28px; font-weight: bold; color: white;">{value}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        with st.expander("Zeige allgemeine Spielstatistiken"):
                            # Zusammenfassungs-Statistiken
                            # st.header("Zusammenfassung")
                            deaths = stats_dict.get("total_deaths", 0)
                            kills = stats_dict.get("total_kills", 0)
                            if deaths > 0:
                                death_ratio = kills / deaths
                            else:
                                death_ratio = "∞"  # Vermeidung Division durch Null (String-Wert-Rückgabe -> deswegen if-Bedinung in Ausgabe!)
                            
                            death_ratio_value = float(death_ratio) if isinstance(death_ratio, (float, int)) else 0

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                custom_metric("Abschüsse insgesamt", f"{kills:,}".replace(",", "."))
                            with col2:
                                custom_metric("Tode insgesamt", f"{deaths:,}".replace(",", "."))
                            with col3:
                                custom_metric("KD-Ratio", f"{death_ratio_value:.2f}".replace(".", ","))

                            # Spielzeit, Siege, Runden
                            time_played_hours = stats_dict["total_time_played"] / 3600
                            total_wins = stats_dict.get("total_wins", 0)
                            total_rounds_played = stats_dict.get("total_rounds_played", 0)

                            col4, col5, col6 = st.columns(3)
                            with col4:
                                custom_metric("Zeit spielend [h]", f"{time_played_hours:.0f}")
                            with col5:
                                custom_metric("Siege gesamt", f"{total_wins:,}".replace(",", "."))
                            with col6:
                                custom_metric("Gespielte Runden", f"{total_rounds_played:,}".replace(",", "."))

                            # Zusätzlicher Platz durch eine Leerzeile und Padding
                            st.markdown(
                                """
                                <style>
                                .st-expander .stContainer {
                                    padding-bottom: 20px; /* Abstand am unteren Rand */
                                }
                                </style>
                                """,
                                unsafe_allow_html=True,
                            )

                        with st.expander("Zeige Treffer- und Headshot-Statistiken"):
                            # Schussdaten
                            shots_fired = stats_dict.get("total_shots_fired", 0)
                            shots_hit = stats_dict.get("total_shots_hit", 0)
                            headshots = stats_dict.get("total_kills_headshot", 0)
                            shots_missed = shots_fired - shots_hit  # Verfehlte Schüsse direkt berechnen
                            per_shorts_fired = 1
                            if shots_fired > 0:
                                accuracy = shots_hit / shots_fired * 100
                                headshot_ratio = headshots / shots_hit * 100 if shots_hit > 0 else 0
                        
                        
                            col7, col8, col9 = st.columns(3)
                            with col7:
                                custom_metric("Abgefeuerte Schüsse", f"{shots_fired:,}".replace(",", "."))
                            with col8:
                                custom_metric("Treffer", f"{shots_hit:,}".replace(",", "."))
                            with col9:
                                custom_metric("Headshots", f"{headshots:,}".replace(",", "."))

                        
                            col10, col11 = st.columns(2)
                            # Gemeinsame Diagrammgröße
                            figsize = (4, 4)  # Gleiche Größe für beide Diagramme

                            # Hintergrundfarbe Schwarz setzen
                            plt.rcParams['figure.facecolor'] = '#0E1117'
                            
                            with col10:
                                labels = ["Treffer", "Verfehlt"]
                                sizes = [shots_hit, shots_missed]
                                colors = ["#4CAF50", "#FFC107"]
                                explode = (0.1, 0)  # Nur das erste Segment hervorheben

                                fig, ax = plt.subplots(figsize=figsize, dpi=90)
                                ax.set_facecolor("#0E1117")
                                ax.pie(
                                    sizes,
                                    explode=explode,
                                    labels=labels,
                                    colors=colors,
                                    autopct=lambda p: f'{p:.1f}%\n{int(sizes[int(p > 50)]):,.0f}'.replace(',', '.'),
                                    startangle=140,
                                    textprops={'color': "white"},
                                )
                                ax.axis("equal")  # Gleichmäßige Darstellung des Kreises
                                st.pyplot(fig)

                            with col11:
                                headshot_labels = ["Headshots", "Andere Treffer"]
                                headshot_sizes = [headshots, shots_hit - headshots]
                                headshot_colors = ["#2196F3", "#8BC34A"]
                                explode_headshots = (0.1, 0)

                                fig2, ax2 = plt.subplots(figsize=figsize, dpi=100)
                                ax2.set_facecolor("#0E1117")
                                ax2.pie(
                                    headshot_sizes,
                                    explode=explode_headshots,
                                    labels=headshot_labels,
                                    colors=headshot_colors,
                                    autopct=lambda p: f'{p:.1f}%\n{int(headshot_sizes[int(p > 50)]):,.0f}'.replace(',', '.'),
                                    startangle=140,
                                    textprops={'color': "white"},
                                )
                                ax2.axis("equal")
                                st.pyplot(fig2)

                        with st.expander("Zeige Match-Statistiken"):
                            # Matchdaten
                            matches_played = stats_dict.get("total_matches_played", 0)
                            matches_won    = stats_dict.get("total_matches_won", 0)
                            if matches_played > 0:
                                win_ratio = matches_won / matches_played * 100
                            else:
                                win_ratio = "∞"  # Vermeidung Division durch Null (String-Wert-Rückgabe -> deswegen if-Bedinung in Ausgabe!)
                            
                            win_ratio_value = float(win_ratio) if isinstance(win_ratio, (float, int)) else 0

                            col12, col13, col14 = st.columns(3)
                            with col12:
                                custom_metric("Gespielte Matches", f"{matches_played:,}".replace(",", "."))
                            with col13:
                                custom_metric("Gewonnene Matches", f"{matches_won:,}".replace(",", "."))
                            with col14:
                                custom_metric("Siegesquote", f"{win_ratio_value:.1f}".replace(".", ",") + " %")

                            # GG-Daten
                            gg_played = stats_dict.get("total_gg_matches_played", 0)
                            gg_won    = stats_dict.get("total_gg_matches_won", 0)
                            if gg_played > 0:
                                gg_ratio = gg_won / gg_played * 100
                            else:
                                gg_ratio = "∞"  # Vermeidung Division durch Null (String-Wert-Rückgabe -> deswegen if-Bedinung in Ausgabe!)
                            
                            gg_ratio_value = float(gg_ratio) if isinstance(gg_ratio, (float, int)) else 0

                            col15, col16, col17 = st.columns(3)
                            with col15:
                                custom_metric("Gespielte GG-Matches", f"{gg_played:,}".replace(",", "."))
                            with col16:
                                custom_metric("Gewonnene GG-Matches", f"{gg_won:,}".replace(",", "."))
                            with col17:
                                custom_metric("GG-Siegesquote", f"{gg_ratio_value:.1f}".replace(".", ",") + " %")
                            
                            # Zusätzlicher Platz durch eine Leerzeile und Padding
                            st.markdown(
                                """
                                <style>
                                .st-expander .stContainer {
                                    padding-bottom: 20px; /* Abstand am unteren Rand */
                                }
                                </style>
                                """,
                                unsafe_allow_html=True,
                            )
# -----
                    elif len(filtered_stats) > 0 and chosen_app_id == 648800:
                        
                        # Dictionary aus den gefilterten Statistiken, um besser darauf zugreifen zu können 
                        stats_dict = {stat["name"]: stat["value"] for stat in filtered_stats}

                        # Key-Value-Format ausgeben
                        st.write("**Statistiken**")

                        def custom_metric(label, value):
                            st.markdown(
                                f"""
                                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                                    <div style="text-align: left; width: 100%; font-size: 16px; font-weight: normal; color: #6c757d;">{label}</div>
                                    <div style="font-size: 28px; font-weight: bold; color: white;">{value}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        with st.expander("Dunkle Statistik"):
                            deaths = stats_dict.get("stat_player_deaths", 0)
                            custom_metric("Tode", f"{deaths:,}".replace(",", "."))
                        
                            # Zusätzlicher Platz durch eine Leerzeile und Padding
                            st.markdown(
                                """
                                <style>
                                .st-expander .stContainer {
                                    padding-bottom: 20px; /* Abstand am unteren Rand */
                                }
                                </style>
                                """,
                                unsafe_allow_html=True,
                            )
                        
                        with st.expander("Statistiken Tiere"):
                            sharks = stats_dict.get("stat_player_sharkKills", 0)
                            birds = stats_dict.get("stat_player_birdKills", 0)
                            puffer = stats_dict.get("stat_player_pufferKills", 0)
                            stoneBird = stats_dict.get("stat_player_stoneBirdKills", 0)
                            rat = stats_dict.get("stat_player_ratKills", 0)
                            bear = stats_dict.get("stat_player_bearKills", 0)
                            bot = stats_dict.get("stat_player_botKills", 0)
                            anglerFish = stats_dict.get("stat_player_anglerFishKills", 0)
                            boar = stats_dict.get("stat_player_boarKills", 0)

                            bees = stats_dict.get("stat_player_captures_bee", 0)
                            animals = stats_dict.get("stat_player_capturedAnimals", 0)

                            # Überprüfen, ob 'animals' ein Tuple ist und ggf. nur den ersten Wert verwenden
                            if isinstance(animals, tuple):
                                animals = animals[0]  # Extrahiere den ersten Wert aus dem Tuple

                            # Sicherstellen, dass 'animals' eine Zahl ist
                            if isinstance(animals, (int, float)):
                                formatted_value = f"{animals:,}".replace(",", ".")
                            else:
                                formatted_value = "N/A"  # Fallback-Wert, falls 'animals' keine Zahl ist

                            # Daten für das Diagramm
                            animal_kills = {
                                "Haie": sharks,
                                "Vögel": birds,
                                "Kugelfische": puffer,
                                "Steinwurf-Vögel": stoneBird,
                                "Ratten": rat,
                                "Bären": bear,
                                "Roboter": bot,
                                "Anglerfische": anglerFish,
                                "Wildschweine": boar,
                            }

                            # Daten sortieren (absteigend nach Anzahl der Kills)
                            sorted_animals = sorted(animal_kills.items(), key=lambda x: x[1], reverse=True)
                            animals, kills = zip(*sorted_animals)

                            col2, col3 = st.columns(2)
                            with col2:
                                custom_metric("Haie", f"{sharks:,}".replace(",", "."))
                                custom_metric("Vögel", f"{birds:,}".replace(",", "."))
                                custom_metric("Kugelfische", f"{puffer:,}".replace(",", "."))
                                custom_metric("Steinwurf-Vögel", f"{stoneBird:,}".replace(",", "."))
                                custom_metric("Ratten", f"{rat:,}".replace(",", "."))
                                custom_metric("Bären", f"{bear:,}".replace(",", "."))
                                custom_metric("Roboter", f"{bot:,}".replace(",", "."))
                                custom_metric("Anglerfische", f"{anglerFish:,}".replace(",", "."))
                                custom_metric("Wildschweine", f"{boar:,}".replace(",", "."))
                            
                            with col3:
                                # Einen flexiblen Platzhalter für das Diagramm schaffen
                                with st.container():
                                    # Berechne Platzhalter basierend auf Anzahl der Elemente
                                    num_metrics = len(animal_kills)
                                    padding_lines = max(2, num_metrics // 2)  # Automatische Berechnung der Leerzeilen

                                    for _ in range(padding_lines):  
                                        st.write("")  # Leere Zeilen für vertikale Zentrierung

                                    background_color = "#0e1117"  # Dunkler Hintergrund
                                    text_color = "#ffffff"  # Helle Schrift
                                    bar_color = "#4a90e2"  # Blau für die Balken

                                    ## Balkendiagramm erstellen
                                    fig, ax = plt.subplots(figsize=(6, 4))
                                    fig.patch.set_facecolor(background_color)  # Hintergrundfarbe für die gesamte Figur
                                    ax.set_facecolor(background_color)  # Hintergrundfarbe für das Diagramm

                                    ax.barh(animals, kills, color=bar_color)  # Balkenfarbe
                                    ax.set_xlabel("Anzahl Kills", color=text_color)
                                    ax.set_ylabel("Tierart", color=text_color)
                                    ax.set_title("Getötete Tiere (absteigend)", color=text_color)
                                    ax.tick_params(colors=text_color)  # Achsenbeschriftung anpassen
                                    ax.spines["top"].set_color(background_color)  # Entferne obere Rahmenlinie
                                    ax.spines["right"].set_color(background_color)  # Entferne rechte Rahmenlinie
                                    ax.spines["bottom"].set_color(text_color)  # Achsenlinie unten anpassen
                                    ax.spines["left"].set_color(text_color)  # Achsenlinie links anpassen
                                    ax.invert_yaxis()  # Größte Werte oben

                                    # Diagramm in Streamlit anzeigen
                                    st.pyplot(fig, use_container_width=True)

                                    for _ in range(padding_lines):  
                                        st.write("")  # Leere Zeilen nach dem Diagramm für vertikale Balance
                            
                            with col2:
                                custom_metric("Gesammelte Bienenschwärme", f"{bees:,}".replace(",", "."))
                            
                            with col3:
                                custom_metric("Eingefangene Tiere", formatted_value)
                                
                            # Zusätzlicher Platz durch eine Leerzeile und Padding
                            st.markdown(
                                """
                                <style>
                                .st-expander .stContainer {
                                    padding-bottom: 20px; /* Abstand am unteren Rand */
                                }
                                </style>
                                """,
                                unsafe_allow_html=True,
                            )

                        with st.expander("Diverse Statistiken"):
                            instruments = stats_dict.get("stat_player_instrumentNotes_played", 0)
                            fireworks = stats_dict.get("stat_player_fireworks_launched", 0)
                            excevations = stats_dict.get("stat_player_excevations_treasure", 0)
                            token = stats_dict.get("stat_player_token_spend_tangaroa", 0)

                            col4, col5, col6, col7 = st.columns(4)
                            with col4:
                                custom_metric("Gespielte Noten mit Musikinstrumenten", f"{instruments:,}".replace(",", "."))
                            with col5:
                                custom_metric("Abgefeuerte Feuerwerke", f"{fireworks:,}".replace(",", "."))
                            with col6:
                                custom_metric("Ausgegrabene Schätze", f"{excevations:,}".replace(",", "."))
                            with col7:
                                custom_metric("Ausgegebene Tokens auf Tangaroa", f"{token:,}".replace(",", "."))

                            paint = stats_dict.get("stat_build_paintCount", 0)
                            remove = stats_dict.get("stat_build_removeCount", 0)
                            hook = stats_dict.get("stat_player_hookCount", 0)
                            foundation = stats_dict.get("stat_build_foundationCount", 0)

                            col8, col9, col10, col11 = st.columns(4)
                            with col8:
                                custom_metric("Bemalte Objekte", f"{paint:,}".replace(",", "."))
                            with col9:
                                custom_metric("Entfernte Strukturen", f"{remove:,}".replace(",", "."))
                            with col10:
                                custom_metric("Verwendung des Hakens", f"{hook:,}".replace(",", "."))
                            with col11:
                                custom_metric("Gebaute Fundamente", f"{foundation:,}".replace(",", "."))

                            # Zusätzlicher Platz durch eine Leerzeile und Padding
                            st.markdown(
                                """
                                <style>
                                .st-expander .stContainer {
                                    padding-bottom: 20px; /* Abstand am unteren Rand */
                                }
                                </style>
                                """,
                                unsafe_allow_html=True,
                            )

                        with st.expander("Seilrutschen-Statistiken"):
                            distance = stats_dict.get("stat_player_zipline_distance", 0)
                            distanceOneGo = stats_dict.get("stat_player_zipline_distanceOneGo", 0)

                            col12, col13 = st.columns(2)
                            with col12:
                                custom_metric("Zurückgelegte Distanz Seilrutsche", f"{distance:,}".replace(",", "."))
                            with col13:
                                custom_metric("Maximale Distanz Seilrutsche", f"{distanceOneGo:,}".replace(",", "."))
                            
                            # Zusätzlicher Platz durch eine Leerzeile und Padding
                            st.markdown(
                                """
                                <style>
                                .st-expander .stContainer {
                                    padding-bottom: 20px; /* Abstand am unteren Rand */
                                }
                                </style>
                                """,
                                unsafe_allow_html=True,
                            )
# -----

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