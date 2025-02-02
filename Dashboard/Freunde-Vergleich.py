#Freunde-Vergleich
with tabs[3]:
    st.header("👥 Freunde-Vergleich")

    steam_id_1 = st.text_input(label="STEAM-ID", placeholder="--- Gib hier die erste SteamID64 ein ---", label_visibility="hidden")
    steam_id_2 = st.text_input(label="STEAM-ID", placeholder="--- Gib hier die zweite SteamID64 ein ---", label_visibility="hidden")
    button_compare = st.button("Vergleichen")

    if steam_id_1 and steam_id_2:
        st.write(f"📊 **Vergleich von Steam-IDs:** `{steam_id_1}` & `{steam_id_2}`")
        st.write("🔄 **Lade Benutzer- und Spiele-Daten...**")

        with st.spinner("Daten werden geladen..."):
            result_1 = user_owned_games.get_owned_games(API_KEY, steam_id_1)
            info_result_1 = user_info.get_user_info(API_KEY, steam_id_1)
            result_2 = user_owned_games.get_owned_games(API_KEY, steam_id_2)
            info_result_2 = user_info.get_user_info(API_KEY, steam_id_2)

        # Fehlerprüfung für Benutzerinfos
        if "error" in info_result_1:
            st.error(f"❌ Fehler bei der ersten SteamID: {info_result_1['error']}")
        elif "error" in info_result_2:
            st.error(f"❌ Fehler bei der zweiten SteamID: {info_result_2['error']}")
        else:
            st.subheader("🔍 **Benutzerinformationen im Vergleich**")
            col1, col2 = st.columns(2)  # Zwei Spalten für die Benutzer

            for col, info_result, steam_id in zip([col1, col2], [info_result_1, info_result_2], [steam_id_1, steam_id_2]):
                with col:
                    st.write(f"**Benutzername:** {info_result['personaname']}")
                    st.write(f"**Letzter Logoff:** {info_result['lastlogoff']}")
                    st.write(f"**Konto erstellt am:** {info_result['timecreated']}")
                    st.write(f"**Tage seit Kontoerstellung:** {info_result['days_since_creation']}")

                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: center; align-items: center; height: 100%; margin-top: -10px;">
                            <img src="{info_result['avatarfull']}" alt="Avatar" style="width: 100px; border-radius: 0%;">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # Fehlerprüfung für Spielelisten
            if "error" in result_1:
                st.error(f"❌ Fehler bei der ersten SteamID: {result_1['error']}")
            elif "error" in result_2:
                st.error(f"❌ Fehler bei der zweiten SteamID: {result_2['error']}")
            else:
                games_1 = result_1.get("response", {}).get("games", [])
                games_2 = result_2.get("response", {}).get("games", [])

                if not games_1:
                    st.warning("⚠️ Keine Spiele für die erste SteamID gefunden.")
                elif not games_2:
                    st.warning("⚠️ Keine Spiele für die zweite SteamID gefunden.")
                else:
                    # DataFrames erstellen und sortieren
                    df_1 = pd.DataFrame(games_1)[["appid", "name", "playtime_forever"]].rename(columns={"name": "Name", "playtime_forever": "Spielzeit in Stunden"})
                    df_2 = pd.DataFrame(games_2)[["appid", "name", "playtime_forever"]].rename(columns={"name": "Name", "playtime_forever": "Spielzeit in Stunden"})

                    # Minuten in Stunden umwandeln
                    df_1["Playtime (Hours)"] = df_1["Playtime (Hours)"] / 60
                    df_2["Playtime (Hours)"] = df_2["Playtime (Hours)"] / 60

                    # Spiele aus der definierten Liste filtern
                    valid_games = {game["appid"]: game["name"] for game in games}
                    df_1 = df_1[df_1["appid"].isin(valid_games.keys())]
                    df_2 = df_2[df_2["appid"].isin(valid_games.keys())]

                    # Gemeinsame Spiele ermitteln
                    common_games = pd.merge(df_1, df_2, on=["appid", "Name"], suffixes=("_Player1", "_Player2"))

                    st.subheader("🎮 **Gemeinsame Spiele**")
                    if not common_games.empty:
                        # Spalten für Tabelle (links) und Grafik (rechts)
                        col1, col2 = st.columns([1.5, 1])  # Verhältnis: 1.5 : 1

                        with col1:  # **Tabelle links**
                            st.dataframe(common_games[["Name", "Spielzeit in Stunden_Player1", "Spielzeit in Stunden_Player2"]].sort_values(by="Spielzeit in Stunden_Player1", ascending=False))

                        with col2:  # **Graphik rechts**
                            # Balkendiagramm mit den Top 5 gemeinsamen Spielen nach Spielzeit von Spieler 1
                            top_5_games = common_games.sort_values(by="Spielzeit in Stunden_Player1", ascending=False).head(5)

                            fig, ax = plt.subplots(figsize=(6, 4))  # Kleinere Grafik für Spaltenlayout
                            bar_width = 0.4
                            indices = range(len(top_5_games))

                            ax.bar([i - bar_width/2 for i in indices], top_5_games["Spielzeit in Stunden_Player1"], width=bar_width, label="Spieler 1", alpha=0.7)
                            ax.bar([i + bar_width/2 for i in indices], top_5_games["Spielzeit in Stunden_Player2"], width=bar_width, label="Spieler 2", alpha=0.7)

                            ax.set_xticks(indices)
                            ax.set_xticklabels(top_5_games["Name"], rotation=45, ha="right")
                            ax.set_xlabel("Spiel")
                            ax.set_ylabel("Spielzeit (Stunden)")
                            ax.set_title("Top 5 gemeinsame Spiele nach Spielzeit (Spieler 1)")
                            ax.legend()

                            st.pyplot(fig)
                        
                        # Auswahlbox mit den gefilterten Spielen
                        selected_game = st.selectbox(
                            "🎯 Wähle ein Spiel für weitere Statistiken:",
                            common_games["Name"].tolist()
                        )

                        if selected_game:
                            app_id = str(common_games[common_games["Name"] == selected_game]["appid"].values[0])

                            if app_id in STAT_MAPPING:
                                # Abrufen der Statistiken für beide Spieler
                                stats_player1 = user_stats.get_user_stats_for_game(API_KEY, steam_id_1, app_id)
                                stats_player2 = user_stats.get_user_stats_for_game(API_KEY, steam_id_2, app_id)

                                # Sicherstellen, dass wir keine Listen haben
                                stats_player1 = convert_list_to_dict(stats_player1)
                                stats_player2 = convert_list_to_dict(stats_player2)

                                if isinstance(stats_player1, dict) and isinstance(stats_player2, dict):
                                    st.subheader(f"📊 **Vergleich für {selected_game}**")

                                    # Nur die relevanten Statistiken aus STAT_MAPPING anzeigen
                                    relevant_stats = STAT_MAPPING[app_id]
                                    filtered_stats = [stat for stat in relevant_stats if stat in stats_player1 and stat in stats_player2]

                                    if filtered_stats:
                                        comparison_data = {
                                            "Statistik": [STAT_LABELS.get(stat, stat) for stat in filtered_stats],  # Labels umbenennen
                                            "Spieler 1": [stats_player1.get(stat, "N/A") for stat in filtered_stats],
                                            "Spieler 2": [stats_player2.get(stat, "N/A") for stat in filtered_stats]
                                        }
                                        df_comparison = pd.DataFrame(comparison_data)

                                        st.dataframe(df_comparison.style.format({"Spieler 1": "{:.1f}", "Spieler 2": "{:.1f}"}))

                                    else:
                                        st.warning("📉 Keine passenden Statistikwerte gefunden.")
                                else:
                                    st.warning("⚠️ Keine gültigen Statistikdaten verfügbar.")
                            else:
                                st.warning("⚠️ Keine Statistik-Daten für dieses Spiel im Mapping hinterlegt.")
                    else:
                        st.write("⚠️ **Keine gemeinsamen Spiele aus der definierten Liste gefunden.**")