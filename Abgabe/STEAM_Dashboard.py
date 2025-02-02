# ------------------------------------------------------------------------------------------------------------
# Import benötigter Bibliotheken
import requests
import pandas as pd
import numpy as np #change Lucian
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px
import matplotlib.ticker as mticker
import user_owned_games
import user_info
import user_game
import user_dataframe as df
import numpy as np
from curve_helper import create_percentile_curve
# ------------------------------------------------------------------------------------------------------------
bool_id = False
# ------------------------------------------------------------------------------------------------------------
# Wide Mode
st.set_page_config(layout="wide") # Aktiviert den Wide Mode
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
# Streamlit App

col1, col2 = st.columns ([5, 1])
with col1:
    st.title("Steam Dashboard by Gamescope")
with col2:
    st.image("Gamescope.png", width=100)
    # st.markdown(
    #     "<div style='display: flex; justify-content: flex-end;'>",
    #     unsafe_allow_html=True
    # )
    # st.image("Gamescope.png", width=100)
    # st.markdown("</div>", unsafe_allow_html=True)

# Tabs erstellen
tabs = st.tabs(["Profilstatistiken", "In-Game-Statistiken", "Community-Vergleich", "Freunde-Vergleich", "Finde neue Freunde und Games"])

# API Key (du kannst eine sichere Methode verwenden, um den Schlüssel zu speichern)
API_KEY = "F06E65C071B7ABDE4CE3B531A06123E2"
# Key Paul: DB15759E609C1E342536A6973593A57F
# Key Lucian: F06E65C071B7ABDE4CE3B531A06123E2
# Key Viki: 3DD952ECA5D79C777FD0377B118779A0
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
        "total_gg_matches_played",
        #---
        "total_hits_ak47",
        "total_hits_aug",
        "total_hits_awp",
        "total_hits_bizon",
        "total_hits_deagle",
        "total_hits_elite",
        "total_hits_famas",
        "total_hits_fiveseven",
        "total_hits_g3sg1",
        "total_hits_galilar",
        "total_hits_glock",
        "total_hits_hkp2000",
        "total_hits_m249",
        "total_hits_m4a1",
        "total_hits_mac10",
        "total_hits_mag7",
        "total_hits_mp7",
        "total_hits_mp9",
        "total_hits_negev",
        "total_hits_nova",
        "total_hits_p250",
        "total_hits_p90",
        "total_hits_sawedoff",
        "total_hits_scar20",
        "total_hits_sg556",
        "total_hits_ssg08",
        "total_hits_tec9",
        "total_hits_ump45",
        "total_hits_xm1014",
        #---
        "total_kills_ak47",
        "total_kills_aug",
        "total_kills_awp",
        "total_kills_bizon",
        "total_kills_deagle",
        "total_kills_elite",
        "total_kills_famas",
        "total_kills_fiveseven",
        "total_kills_g3sg1",
        "total_kills_galilar",
        "total_kills_glock",
        "total_kills_hkp2000",
        "total_kills_m249",
        "total_kills_m4a1",
        "total_kills_mac10",
        "total_kills_mag7",
        "total_kills_mp7",
        "total_kills_mp9",
        "total_kills_negev",
        "total_kills_nova",
        "total_kills_p250",
        "total_kills_p90",
        "total_kills_sawedoff",
        "total_kills_scar20",
        "total_kills_sg556",
        "total_kills_ssg08",
        "total_kills_tec9",
        "total_kills_ump45",
        "total_kills_xm1014",
        #---
        "total_shots_ak47",
        "total_shots_aug",
        "total_shots_awp",
        "total_shots_bizon",
        "total_shots_deagle",
        "total_shots_elite",
        "total_shots_famas",
        "total_shots_fiveseven",
        "total_shots_g3sg1",
        "total_shots_galilar",
        "total_shots_glock",
        "total_shots_hkp2000",
        "total_shots_m249",
        "total_shots_m4a1",
        "total_shots_mac10",
        "total_shots_mag7",
        "total_shots_mp7",
        "total_shots_mp9",
        "total_shots_negev",
        "total_shots_nova",
        "total_shots_p250",
        "total_shots_p90",
        "total_shots_sawedoff",
        "total_shots_scar20",
        "total_shots_sg556",
        "total_shots_ssg08",
        "total_shots_tec9",
        "total_shots_ump45",
        "total_shots_xm1014",
        #---
        "total_kills_hegrenade",
        "total_kills_knife_fight",
        "total_kills_knife",
        "total_kills_molotov",
        "total_kills_decoy",
        "total_kills_taser",
        "total_shots_taser",
        #---
        "total_defused_bombs",
        "total_planted_bombs",
        "total_rescued_hostages",
        #---
        "total_rounds_map_ar_baggage",
        "total_rounds_map_ar_monastery",
        "total_rounds_map_ar_shoots",
        "total_rounds_map_cs_assault",
        "total_rounds_map_cs_italy",
        "total_rounds_map_cs_militia",
        "total_rounds_map_cs_office",
        "total_rounds_map_de_aztec",
        "total_rounds_map_de_cbble",
        "total_rounds_map_de_dust",
        "total_rounds_map_de_dust2",
        "total_rounds_map_de_inferno",
        "total_rounds_map_de_lake",
        "total_rounds_map_de_nuke",
        "total_rounds_map_de_safehouse",
        "total_rounds_map_de_stmarc",
        "total_rounds_map_de_sugarcane",
        "total_rounds_map_de_train",
        "total_rounds_map_de_vertigo"
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
    #-
    "total_hits_ak47": "Treffer ak47",
    "total_hits_aug": "Treffer aug",
    "total_hits_awp": "Treffer awp",
    "total_hits_bizon": "Treffer bizon",
    "total_hits_deagle": "Treffer deagle",
    "total_hits_elite": "Treffer elite",
    "total_hits_famas": "Treffer famas",
    "total_hits_fiveseven": "Treffer fiveseven",
    "total_hits_g3sg1": "Treffer g3sg1",
    "total_hits_galilar": "Treffer galilar",
    "total_hits_glock": "Treffer glock",
    "total_hits_hkp2000": "Treffer hkp2000",
    "total_hits_m249": "Treffer m249",
    "total_hits_m4a1": "Treffer m4a1",
    "total_hits_mac10": "Treffer mac10",
    "total_hits_mag7": "Treffer mag7",
    "total_hits_mp7": "Treffer mp7",
    "total_hits_mp9": "Treffer mp9",
    "total_hits_negev": "Treffer negev",
    "total_hits_nova": "Treffer nova",
    "total_hits_p250": "Treffer p250",
    "total_hits_p90": "Treffer p90",
    "total_hits_sawedoff": "Treffer sawedoff",
    "total_hits_scar20": "Treffer scar20",
    "total_hits_sg556": "Treffer sg445",
    "total_hits_ssg08": "Treffer ssg08",
    "total_hits_tec9": "Treffer tec9",
    "total_hits_ump45": "Treffer ump45",
    "total_hits_xm1014": "Treffer xm1014",
    #-
    "total_kills_ak47": "Kills ak47",
    "total_kills_aug": "Kills aug",
    "total_kills_awp": "Kills awp",
    "total_kills_bizon": "Kills bozon",
    "total_kills_deagle": "Kills deagle",
    "total_kills_elite": "Kills elite",
    "total_kills_famas": "Kills famas",
    "total_kills_fiveseven": "Kills fiveseven",
    "total_kills_g3sg1": "Kills g3sg1",
    "total_kills_galilar": "Kills galilar",
    "total_kills_glock": "Kills glock",
    "total_kills_hkp2000": "Kills hkp2000",
    "total_kills_m249": "Kills m249",
    "total_kills_m4a1": "Kills m4a1",
    "total_kills_mac10": "Kills mac10",
    "total_kills_mag7": "Kills mag7",
    "total_kills_mp7": "Kills mp7",
    "total_kills_mp9": "Kills mp9",
    "total_kills_negev": "Kills negev",
    "total_kills_nova": "Kills nova",
    "total_kills_p250": "Kills p250",
    "total_kills_p90": "Kills p90",
    "total_kills_sawedoff": "Kills sawedoff",
    "total_kills_scar20": "Kills scar20",
    "total_kills_sg556": "Kills sg556",
    "total_kills_ssg08": "Kills ssg08",
    "total_kills_tec9": "Kills tec9",
    "total_kills_ump45": "Kills ump45",
    "total_kills_xm1014": "Kills xm1014",
    #-
    "total_shots_ak47": "Schüsse ak47",
    "total_shots_aug": "Schüsse aug",
    "total_shots_awp": "Schüsse awp",
    "total_shots_bizon": "Schüsse bozon",
    "total_shots_deagle": "Schüsse deagle",
    "total_shots_elite": "Schüsse elite",
    "total_shots_famas": "Schüsse famas",
    "total_shots_fiveseven": "Schüsse fiveseven",
    "total_shots_g3sg1": "Schüsse g3sg1",
    "total_shots_galilar": "Schüsse galilar",
    "total_shots_glock": "Schüsse glock",
    "total_shots_hkp2000": "Schüsse hkp2000",
    "total_shots_m249": "Schüsse m249",
    "total_shots_m4a1": "Schüsse m4a1",
    "total_shots_mac10": "Schüsse mac10",
    "total_shots_mag7": "Schüsse mag7",
    "total_shots_mp7": "Schüsse mp7",
    "total_shots_mp9": "Schüsse mp9",
    "total_shots_negev": "Schüsse negev",
    "total_shots_nova": "Schüsse nova",
    "total_shots_p250": "Schüsse p250",
    "total_shots_p90": "Schüsse p90",
    "total_shots_sawedoff": "Schüsse sawedoff",
    "total_shots_scar20": "Schüsse scar20",
    "total_shots_sg556": "Schüsse sg556",
    "total_shots_ssg08": "Schüsse ssg08",
    "total_shots_tec9": "Schüsse tec9",
    "total_shots_ump45": "Schüsse ump45",
    "total_shots_xm1014": "Schüsse xm1014",
    #-
    "total_kills_hegrenade": "Kills Handgranate",
    "total_kills_knife_fight": "Kills Messerkampf",
    "total_kills_knife": "Kills Messer",
    "total_kills_molotov": "Kills Molotov",
    "total_kills_decoy": "Kills Köder/Fale",
    "total_kills_taser": "Kills Taser",
    "total_shots_taser": "Schüsse Taser",
    #-
    "total_defused_bombs": "Anzahl entschäfter Bomben",
    "total_planted_bombs": "Anzahl platzierter Bomben",
    "total_rescued_hostages": "Anzahl geretteter Geiseln",
    #-
    "total_rounds_map_ar_baggage": "Runden auf der Map baggage",
    "total_rounds_map_ar_monastery": "Runden auf der Map monastery",
    "total_rounds_map_ar_shoots": "Runden auf der Map shoots",
    "total_rounds_map_cs_assault": "Runden auf der Map assault",
    "total_rounds_map_cs_italy": "Runden auf der Map italy",
    "total_rounds_map_cs_militia": "Runden auf der Map militia",
    "total_rounds_map_cs_office": "Runden auf der Map office",
    "total_rounds_map_de_aztec": "Runden auf der Map aztec",
    "total_rounds_map_de_cbble": "Runden auf der Map cbble",
    "total_rounds_map_de_dust": "Runden auf der Map dust",
    "total_rounds_map_de_dust2": "Runden auf der Map dust2",
    "total_rounds_map_de_inferno": "Runden auf der Map inferno",
    "total_rounds_map_de_lake": "Runden auf der Map lake",
    "total_rounds_map_de_nuke": "Runden auf der Map nuke",
    "total_rounds_map_de_safehouse": "Runden auf der Map safehouse",
    "total_rounds_map_de_stmarc": "Runden auf der Map stmarc",
    "total_rounds_map_de_sugarcane": "Runden auf der Map sugarcane",
    "total_rounds_map_de_train": "Runden auf der Map train",
    "total_rounds_map_de_vertigo": "Runden auf der Map vertigo",
    # ---
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
    # ---
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
    # ---
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
    st.header("👤 Profilstatistiken")
    # st.subheader("Gib deine Steam-ID ein, um deine Profilstatistiken zu sehen und die weiteren Funktionen nutzen zu können:")

    # # CSS für die vertikale Ausrichtung und zentrierten Text im Eingabefeld
    # st.markdown(
    #     """
    #     <style>
    #     input {
    #         text-align: center; /* Zentriere den Text */
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )

    # Nutze Markdown mit weniger Padding für kleinere Abstände
    st.markdown(
        '<p style="margin-bottom: 5px; font-size: 18px;">'
        'Gib deine Steam-ID ein, um deine Profilstatistiken zu sehen und die weiteren Funktionen nutzen zu können:'
        '</p>',
        unsafe_allow_html=True
    )

    # CSS für die Input-Box, um Padding/Abstand zu reduzieren und Text zu zentrieren
    st.markdown(
        """
        <style>
        div.stTextInput>div>div>input {
            text-align: center; /* Zentriere den Text */
            padding: 5px; /* Reduziere Innenabstand */
            margin-top: -10px; /* Abstand zur Überschrift verkleinern */
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
                # st.write(f"**Tage seit Kontoerstellung:** {info_result['days_since_creation']}")
                st.write(f"**Tage seit Kontoerstellung:** {info_result['days_since_creation']:,}".replace(",", "."))


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
                st.subheader("🕹️ Spielinformationen")

                df_games = df.convert_to_dataframe(games)[["Name", "Playtime (Hours)"]]
                df_games_cluster = df.convert_to_dataframe(games)[["AppID", "Name", "Playtime (Minutes)"]] #change Lucian
                bool_id = True # change Lucian

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
                st.write(f"**Anzahl aller Spiele:** {total_games:,}".replace(",", "."))
                # st.write(f"**Gesamtsumme der Spielzeit [Stunden]:** {total_playtime_hours:.2f}")
                # st.write(f"**Gesamtsumme der Spielzeit:** {int(total_playtime_hours)} Stunden und {int(total_playtime_minutes % 60)} Minuten")
                st.write(f"**Gesamtsumme der Spielzeit:** {int(total_playtime_hours):,}".replace(",", ".") + f" Stunden und {int(total_playtime_minutes % 60)} Minuten")
                st.write(f"**Durchschnittliche tägliche Spielzeit:** {int(avg_daily_playtime_hours)} Stunden und {int(avg_daily_playtime_minutes % 60)} Minuten")
                # st.write(f"**Gesamtsumme der Spielzeit [Tage]:** {total_playtime_days:.0f}")
                st.write(f"**Gesamtsumme der Spielzeit [Tage]:** {total_playtime_days:,.0f}".replace(",", "."))
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

                    df_display = df_games.copy()
                    st.markdown('<div class="centered-table">', unsafe_allow_html=True)
                    df_display.iloc[:, 1] = df_display.iloc[:, 1].apply(lambda x: f"{int(x):,}".replace(",", "."))
                    st.dataframe(df_display)
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
                        text_auto=True,
                        color_discrete_sequence=["#8d2c91"]
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
    st.header("🎮 In-Game-Statistiken")

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

                        with st.expander("♟️ Allgemeine Spielstatistiken"):
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
                                custom_metric("Zeit spielend [h]", f"{time_played_hours:,.0f}".replace(",", "."))
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
                        
                        with st.expander("⚔️ Match-Statistiken"):
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

                        with st.expander("🎯 Treffer- und Headshot-Statistiken"):
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
                                colors = ["#8d2c91", "#68D2FA"]
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
                                headshot_sizes = [headshots, max(shots_hit - headshots, 0)]
                                headshot_colors = ["#b66bb2", "#d4a3d9"]
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

                        with st.expander("🔫 Waffen-Statistiken"):
                            # Waffendaten
                            # Custom CSS für vertikale Zentrierung der Tabelle
                            st.markdown(
                                """
                                <style>
                                .table-container {
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                    height: 100%;  /* Volle Höhe für vertikale Zentrierung */
                                }
                                </style>
                                """,
                                unsafe_allow_html=True,
                            )
                            # Liste aller Waffen
                            weapons = [
                                "ak47", "aug", "awp", "bizon", "deagle", "elite", "famas", "fiveseven", "g3sg1", "galilar",
                                "glock", "hkp2000", "m249", "m4a1", "mac10", "mag7", "mp7", "mp9", "negev", "nova",
                                "p250", "p90", "sawedoff", "scar20", "sg556", "ssg08", "tec9", "ump45", "xm1014"
                            ]

                            # Liste für die Ergebnisse
                            weapon_stats = []

                            for weapon in weapons:
                                hits = stats_dict.get(f"total_hits_{weapon}", 0)
                                kills = stats_dict.get(f"total_kills_{weapon}", 0)
                                shots = stats_dict.get(f"total_shots_{weapon}", 1)  # Division durch 0 vermeiden

                                accuracy = hits / shots  # Trefferquote
                                efficiency = kills / shots  # Effektivität

                                weapon_stats.append([weapon, hits, kills, shots, accuracy, efficiency])
                            
                            # Nach Accuracy und Efficiency sortieren (hohe Werte zuerst)
                            sorted_weapon_stats = sorted(weapon_stats, key=lambda x: (x[5], x[4]), reverse=True)
                            
                            # Daten für das Netzdiagramm vorbereiten
                            labels = [w[0] for w in sorted_weapon_stats]  
                            accuracy_values = [w[4] for w in sorted_weapon_stats]  
                            efficiency_values = [w[5] for w in sorted_weapon_stats]

                            col18, col19 = st.columns(2)

                            with col18:
                                with st.container():
                                    st.markdown("<div class='table-container'><h3 style='text-align: center;'>Top 5 bestgespielte Waffen</h3>", unsafe_allow_html=True)

                                    # Top 5 Waffen ausgeben
                                    top_5_weapons = sorted_weapon_stats[:5]

                                    # In DataFrame umwandeln
                                    df_top5 = pd.DataFrame(top_5_weapons, columns=["Weapon", "Hits", "Kills", "Shots", "Accuracy", "Efficiency"])

                                    # Werte formatieren
                                    df_top5["Hits"] = df_top5["Hits"].apply(lambda x: f"{x:,}".replace(",", "."))
                                    df_top5["Kills"] = df_top5["Kills"].apply(lambda x: f"{x:,}".replace(",", "."))
                                    df_top5["Shots"] = df_top5["Shots"].apply(lambda x: f"{x:,}".replace(",", "."))
                                    df_top5["Accuracy"] = df_top5["Accuracy"].apply(lambda x: f"{x * 100:.1f}%")
                                    df_top5["Efficiency"] = df_top5["Efficiency"].apply(lambda x: f"{x * 100:.1f}%")

                                    # Ausgabe der Top 5 Waffen
                                    st.dataframe(df_top5, use_container_width=True)
                                
                                    st.write("Accuracy = Hits / Shots")
                                    st.write("Efficiency = Kills / Shots")

                            with col19:
                                with st.container():
                                    st.markdown("<h3 style='text-align: center;'>Accuracy vs Efficiency</h3>", unsafe_allow_html=True)

                                    # Erstellen des Netzdiagramms (Radar Chart)
                                    fig = go.Figure()

                                    fig.add_trace(go.Scatterpolar(
                                        r=accuracy_values + [accuracy_values[0]],  # Kreis schließen
                                        theta=labels + [labels[0]],
                                        fill='toself',
                                        name='Accuracy'
                                    ))

                                    fig.add_trace(go.Scatterpolar(
                                        r=efficiency_values + [efficiency_values[0]],  # Kreis schließen
                                        theta=labels + [labels[0]],
                                        fill='toself',
                                        name='Efficiency'
                                    ))

                                    fig.update_layout(
                                        polar=dict(
                                            radialaxis=dict(
                                                visible=True, 
                                                range=[0, max(max(accuracy_values), max(efficiency_values))],
                                                tickfont=dict(color="black")
                                            ),
                                        ),
                                        showlegend=True,
                                        title="Accuracy vs Efficiency für Waffen",
                                        autosize=True  # Automatische Skalierung für bessere Platznutzung
                                    )

                                    st.plotly_chart(fig, use_container_width=True)
                            
                            hegrenade = stats_dict.get("total_kills_hegrenade", 0)
                            kfight = stats_dict.get("total_kills_knife_fight", 0)
                            knife = stats_dict.get("total_kills_knife", 0)
                            molotov = stats_dict.get("total_kills_molotov", 0)
                            decoy = stats_dict.get("total_kills_decoy", 0)
                            ttaser = stats_dict.get("total_shots_taser", 0)
                            taser = stats_dict.get("total_kills_taser", 0)
                            efftaser = taser / ttaser

                            col20, col21, col22 = st.columns(3)
                            with col20:
                                custom_metric("Kills mit der Handgranate", f"{hegrenade:,}".replace(",", "."))
                                custom_metric("Schüsse mit dem Taser", f"{ttaser:,}".replace(",", "."))
                            with col21:
                                custom_metric("Kills mit einem Molotov-Cocktail", f"{molotov:,}".replace(",", "."))
                                custom_metric("Kills mit der Taser", f"{taser:,}".replace(",", "."))
                            with col22:
                                custom_metric("Kills mit einem Köder/Falle", f"{decoy:,}".replace(",", "."))
                                custom_metric("Effizienz mit dem Taser", f"{efftaser:.1%}".replace(",", "."))
                            
                            col23, col24 = st.columns(2)
                            with col23:
                                custom_metric("Kills mit dem Messer", f"{knife:,}".replace(",", "."))
                            with col24:
                                custom_metric("Kills Messerkampf", f"{kfight:,}".replace(",", "."))
                            
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
                        
                        with st.expander("🎲 Sonstige-Statistiken"):
                            # Sonstiges
                            dbombs = stats_dict.get("total_defused_bombs", 0)
                            pbombs = stats_dict.get("total_planted_bombs", 0)
                            hostages = stats_dict.get("total_rescued_hostages", 0)

                            col25, col26, col27 = st.columns(3)
                            with col25:
                                custom_metric("Entschärfte Bomben", f"{dbombs:,}".replace(",", "."))
                            with col26:
                                custom_metric("Platzierte Bomben", f"{pbombs:,}".replace(",", "."))
                            with col27:
                                custom_metric("Anzahl geretteter Geiseln", f"{hostages:,}".replace(",", "."))

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
                        
                        with st.expander("🗺️ Map-Statistik"):
                            # Map-Statistik
                            # Dictionary mit den richtigen Keys für jede Map
                            map_keys = {
                                "baggage": "total_rounds_map_ar_baggage",
                                "monastery": "total_rounds_map_ar_monastery",
                                "shoots": "total_rounds_map_ar_shoots",
                                "assault": "total_rounds_map_cs_assault",
                                "italy": "total_rounds_map_cs_italy",
                                "militia": "total_rounds_map_cs_militia",
                                "office": "total_rounds_map_cs_office",
                                "aztec": "total_rounds_map_de_aztec",
                                "cbble": "total_rounds_map_de_cbble",
                                "dust": "total_rounds_map_de_dust",
                                "dust2": "total_rounds_map_de_dust2",
                                "inferno": "total_rounds_map_de_inferno",
                                "lake": "total_rounds_map_de_lake",
                                "nuke": "total_rounds_map_de_nuke",
                                "safehouse": "total_rounds_map_de_safehouse",
                                "stmarc": "total_rounds_map_de_stmarc",
                                "sugarcane": "total_rounds_map_de_sugarcane",
                                "train": "total_rounds_map_de_train",
                                "vertigo": "total_rounds_map_de_vertigo"
                            }

                            # Liste für die Ergebnisse
                            map_stats = []

                            for map_name, key in map_keys.items():
                                numMap = stats_dict.get(key, 0)
                                map_stats.append([map_name, numMap])

                            # Nach Anzahl der Runden sortieren (hohe Werte zuerst)
                            sorted_map_stats = sorted(map_stats, key=lambda x: x[1], reverse=True)

                            # Listen für Diagramm-Daten
                            map_names = [x[0] for x in sorted_map_stats]
                            rounds_played = [x[1] for x in sorted_map_stats]

                            # Matplotlib Diagramm erstellen
                            fig, ax = plt.subplots(figsize=(10, 5))
                            # Hintergrund auf Schwarz setzen
                            fig.patch.set_facecolor("#0E1117")  # Außenbereich schwarz
                            ax.set_facecolor("#0E1117")  # Innenbereich schwarz
                            # Balkendiagramm mit weißer Schrift
                            bars = ax.barh(map_names, rounds_played, color="#8d2c91")
                            # X-Achse um 15% erweitern, damit die Zahlen weiter rechts stehen
                            max_value = max(rounds_played) if rounds_played else 1  # Falls alle Werte 0 sind, Standardwert setzen
                            ax.set_xlim(0, max_value * 1.10)  # 10% extra Platz auf der X-Achse
                            # Absolute Werte auf die Balken schreiben
                            for bar, value in zip(bars, rounds_played):
                                ax.text(
                                    bar.get_width() + (max_value * 0.02),  # Position direkt neben dem Balken
                                    bar.get_y() + bar.get_height() / 2,  # Zentrieren in der Mitte des Balkens
                                    # str(value),  # Wert als String
                                    f"{value:,}".replace(",", "."),  # Tausendertrennzeichen anpassen
                                    va="center",
                                    ha="left",
                                    color="white",
                                    fontsize=8,
                                )
                            # Achsenbeschriftung, Titel und Werte in Weiß setzen
                            ax.set_xlabel("Anzahl der gespielten Runden", color="white")
                            ax.set_ylabel("Maps", color="white")
                            ax.set_title("Rundenanzahl pro Map", color="white")
                            # Achsenwerte in Weiß setzen
                            ax.tick_params(axis="x", colors="white")
                            ax.tick_params(axis="y", colors="white")
                            # Achsen invertieren für bessere Lesbarkeit
                            ax.invert_yaxis()  
                            # Achsenbeschriftung formatieren
                            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
                            # Rahmen um das Diagramm entfernen
                            ax.spines["top"].set_visible(False)
                            ax.spines["right"].set_visible(False)
                            ax.spines["left"].set_visible(False)
                            ax.spines["bottom"].set_visible(False)

                            # Diagramm in Streamlit anzeigen
                            st.pyplot(fig)

                            # # Ausgabe der sortierten Statistik
                            # for map_name, num_rounds in sorted_map_stats:
                            #     st.write(f"{map_name}: {num_rounds} Runden")
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

                        with st.expander("⚰️ Dunkle Statistik"):
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
                        
                        with st.expander("🦈 Statistiken Tiere"):
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

                                    ax.barh(animals, kills, color="#8d2c91")  # Balkenfarbe
                                    ax.set_xlabel("Anzahl Kills", color=text_color)
                                    ax.set_ylabel("Tierart", color=text_color)
                                    ax.set_title("Getötete Tiere (absteigend)", color=text_color)
                                    ax.tick_params(colors=text_color)  # Achsenbeschriftung anpassen
                                    ax.spines["top"].set_color(background_color)  # Entferne obere Rahmenlinie
                                    ax.spines["right"].set_color(background_color)  # Entferne rechte Rahmenlinie
                                    ax.spines["bottom"].set_color(text_color)  # Achsenlinie unten anpassen
                                    ax.spines["left"].set_color(text_color)  # Achsenlinie links anpassen
                                    ax.invert_yaxis()  # Größte Werte oben

                                    # Achsenbeschriftung formatieren
                                    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
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

                        with st.expander("🎲 Diverse Statistiken"):
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

                        with st.expander("🧗‍♂️⛓️ Seilrutschen-Statistiken"):
                            distance = stats_dict.get("stat_player_zipline_distance", 0)
                            distanceOneGo = stats_dict.get("stat_player_zipline_distanceOneGo", 0)

                            col12, col13 = st.columns(2)
                            with col12:
                                custom_metric("Zurückgelegte Distanz Seilrutsche [m]", f"{distance:,}".replace(",", "."))
                            with col13:
                                custom_metric("Maximale Distanz Seilrutsche [m]", f"{distanceOneGo:,}".replace(",", "."))
                            
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
                    elif len(filtered_stats) > 0 and chosen_app_id == 221100:
                        
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

                        with st.expander("🍗 Nahrungs-Statistiken"):
                            eat = stats_dict.get("STAT_ACTION_EAT", 0)
                            drink = stats_dict.get("STAT_ACTION_DRINK", 0)
                            steak = stats_dict.get("STAT_ACTION_COOK_STEAK", 0)

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                custom_metric("Aktionen, bei denen Nahrung gegessen wurde", f"{eat:,}".replace(",", "."))
                            with col2:
                                custom_metric("Aktionen, bei denen Wasser oder andere Flüssigkeiten getrunken wurden", f"{drink:,}".replace(",", "."))
                            with col3:
                                custom_metric("Anzahl der gekochten Steaks", f"{steak:,}".replace(",", "."))
                            
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
                        
                        with st.expander("🛠️ Praktische-Statistiken"):
                            fire = stats_dict.get("STAT_ACTION_IGNITE_FIRE_MATCHBOX", 0)
                            drill = stats_dict.get("STAT_ACTION_IGNITE_FIRE_HAND_DRILL", 0)
                            gear = stats_dict.get("STAT_ACTION_EQUIP_GEAR", 0)
                            shave = stats_dict.get("STAT_ACTION_SHAVE", 0)
                            deer = stats_dict.get("STAT_ACTION_GUT_DEER", 0)

                            col4, col5 = st.columns(2)
                            with col4:
                                custom_metric("Anzahl der entzündeten Feuer mit Streichhölzern", f"{fire:,}".replace(",", "."))
                            with col5:
                                custom_metric("Anzahl der entzündeten Feuer mit einem Handbohrer", f"{drill:,}".replace(",", "."))

                            col6, col7, col8 = st.columns(3)
                            with col6:
                                custom_metric("Anzahl der Aktionen, bei denen Ausrüstung angelegt wurde", f"{gear:,}".replace(",", "."))
                            with col7:
                                custom_metric("Anzahl der durchgeführten Rasuren", f"{shave:,}".replace(",", "."))
                            with col8:
                                custom_metric("Anzahl der ausgeweideten Hirsche", f"{deer:,}".replace(",", "."))
                            
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

                        with st.expander("⛑️ Überlebens-Statistiken"):
                            meds = stats_dict.get("STAT_ACTION_APPLY_MEDS_ON_SURVIVOR", 0)
                            distance = stats_dict.get("STAT_SURVIVOR_KILL_MAX_DIST", 0)
                            ikill = stats_dict.get("STAT_INFECTED_KILL_COUNT", 0)
                            skill = stats_dict.get("STAT_INFECTED_SOLDIER_KILL_COUNT", 0)
                            mkill = stats_dict.get("STAT_SURVIVOR_MELEE_KILL_COUNT", 0)
                            ihead = stats_dict.get("STAT_INFECTED_HEADSHOT_COUNT", 0)
                            shead = stats_dict.get("STAT_SURVIVOR_HEADSHOT_COUNT", 0)
                            heads = stats_dict.get("STAT_HEADSHOT_COUNT", 0)

                            col9, col10 = st.columns(2)
                            with col9:
                                custom_metric("Anzahl der Anwendungen von Medikamenten auf andere Überlebende", f"{meds:,}".replace(",", "."))
                            with col10:
                                custom_metric("Maximale Distanz, aus der ein Überlebender getötet wurde", f"{distance:,}".replace(",", "."))

                            col11, col12, col13 = st.columns(3)
                            with col11:
                                custom_metric("Anzahl der getöteten Infizierten", f"{ikill:,}".replace(",", "."))
                            with col12:
                                custom_metric("Anzahl der getöteten infizierten Soldaten", f"{skill:,}".replace(",", "."))
                            with col13:
                                custom_metric("Anzahl der getöteten Überlebenden mit Nahkampfwaffen", f"{mkill:,}".replace(",", "."))
                            
                            col14, col15, col16 = st.columns(3)
                            with col14:
                                custom_metric("Anzahl der Kopfschüsse auf Infizierte", f"{ihead:,}".replace(",", "."))
                            with col15:
                                custom_metric("Anzahl der Kopfschüsse auf Überlebende", f"{shead:,}".replace(",", "."))
                            with col16:
                                custom_metric("Gesamtanzahl aller Kopfschüsse", f"{heads:,}".replace(",", "."))
                            
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
                    elif len(filtered_stats) > 0 and chosen_app_id == 222880:
                        
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

                        with st.expander("🥊 Kompetitiver Modus - Statistiken"):
                            totalKills = stats_dict.get("TotalKills", 0)
                            totalCaptures = stats_dict.get("TotalCaptures", 0)
                            totalMVP = stats_dict.get("TotalMVPs", 0)
                            totalHeroCaptures = stats_dict.get("TotalHeroCaptures", 0)

                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                custom_metric("Gesamtanzahl der Kills im kompetitiven Modus", f"{totalKills:,}".replace(",", "."))
                            with col2:
                                custom_metric("Gesamtanzahl der eroberten Ziele im kompetitiven Modus", f"{totalCaptures:,}".replace(",", "."))
                            with col3:
                                custom_metric("Gesamtanzahl der MVP-Auszeichnungen im kompetitiven Modus", f"{totalMVP:,}".replace(",", "."))
                            with col4:
                                custom_metric("Gesamtanzahl der entscheidenden/heldenhaften Eroberungen im kompetitiven Modus", f"{totalHeroCaptures:,}".replace(",", "."))
                            
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
                        
                        with st.expander("🤝🎮 Koop-Modus - Statistiken"):
                            totalKillsCoop = stats_dict.get("TotalKillsCoop", 0)
                            totalCapturesCoop = stats_dict.get("TotalCapturesCoop", 0)
                            totalMVPCoop = stats_dict.get("TotalMVPsCoop", 0)
                            totalHeroCapturesCoop = stats_dict.get("TotalHeroCapturesCoop", 0)

                            col5, col6, col7, col8 = st.columns(4)
                            with col5:
                                custom_metric("Gesamtanzahl der Kills im Koop-Modus", f"{totalKillsCoop:,}".replace(",", "."))
                            with col6:
                                custom_metric("Gesamtanzahl der eroberten Ziele im Koop-Modus", f"{totalCapturesCoop:,}".replace(",", "."))
                            with col7:
                                custom_metric("Gesamtanzahl der MVP-Auszeichnungen im Koop-Modus", f"{totalMVPCoop:,}".replace(",", "."))
                            with col8:
                                custom_metric("Gesamtanzahl der heldenhaften Eroberungen im Koop-Modus", f"{totalHeroCapturesCoop:,}".replace(",", "."))
                            
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
                        
                        with st.expander("📊 Gesamt - Statistiken"):
                            totalKillsAll = stats_dict.get("TotalKillsAll", 0)
                            totalCapturesAll = stats_dict.get("TotalCapturesAll", 0)
                            totalMVPAll = stats_dict.get("TotalMVPsAll", 0)
                            totalHeroCapturesAll = stats_dict.get("TotalHeroCapturesAll", 0)

                            col9, col10, col11, col12 = st.columns(4)
                            with col9:
                                custom_metric("Gesamtanzahl der Kills im Koop-Modus", f"{totalKillsAll:,}".replace(",", "."))
                            with col10:
                                custom_metric("Gesamtanzahl der eroberten Ziele im Koop-Modus", f"{totalCapturesAll:,}".replace(",", "."))
                            with col11:
                                custom_metric("Gesamtanzahl der MVP-Auszeichnungen im Koop-Modus", f"{totalMVPAll:,}".replace(",", "."))
                            with col12:
                                custom_metric("Gesamtanzahl der heldenhaften Eroberungen im Koop-Modus", f"{totalHeroCapturesAll:,}".replace(",", "."))
                            
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

# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------

# Tab "Vergleich mit Spielstatistiken"
with tabs[2]:
    st.header("Vergleich mit der Community")

    # Fehlerhandling: Falls keine Spielstatistik verfügbar ist
    if array_games_updated.empty or "Name" not in array_games_updated.columns:
         st.warning("Es wurde keine Übereinstimmung zwischen den Spielen des/der User/in und unseren Dashboard-Anzeigen gefunden.")
    else:
        # Auswahl eines Spiels (Dropdown, falls Nutzer mehrere Spiele besitzt)
        st.subheader("Wähle ein Spiel für den Vergleich:")
        selected_game = st.selectbox(
            "",
            array_games_updated["Name"].tolist(),
            key="selectbox2"
        )

        # Die entsprechende App-ID finden
        chosen_app_id = array_games_updated.loc[
            array_games_updated["Name"] == selected_game, "App-ID"
        ].values[0]

        if steam_id != "":
            if st.button("Statistiken abrufen und vergleichen"):
                # Lade die Statistikdatei für das gewählte Spiel
                stats_csv = f"{chosen_app_id}_statistische_auswertung.csv"

                try:
                    stats_df = pd.read_csv(stats_csv)
                except FileNotFoundError:
                    st.warning(f"Keine gespeicherten Statistikdaten für Spiel-ID {chosen_app_id} gefunden.")
                    stats_df = None

                if stats_df is not None:
                    # Debugging: Überprüfe, ob Daten aus der API kommen
                    user_game_data = user_game.fetch_in_game_data(API_KEY, steam_id, chosen_app_id)

                    # Funktion zum Abrufen der Statistikwerte aus der CSV
                    def get_stat_values(stat_name):
                        stat_row = stats_df[stats_df["stat"] == stat_name]
                        if not stat_row.empty:
                            return {col: stat_row[col].values[0] for col in stats_df.columns if "%" in col}
                        return None

                    # Vergleichsanzeige mit st.expander
                    def display_comparison(stat_name, display_name, unit="%"):
                        stat_values = get_stat_values(stat_name)
                        if stat_values:
                            median_value = stat_values["50%"]
                            player_value = comparison_metrics[stat_name]

                            # Bestimmen, in welchem Perzentil der Spieler liegt
                            player_percentile = None
                            for p_label, p_value in stat_values.items():
                                if player_value <= p_value:
                                    player_percentile = int(p_label.strip("%"))  # Entfernt das % und wandelt es in eine Zahl um
                                    break

                            # Berechnung der intuitiven Einordnung
                            if player_percentile is not None:
                                top_x_percent = 100 - player_percentile
                                player_position_text = f"Du bist unter den besten {top_x_percent}% der Spieler"
                            else:
                                player_position_text = "Wert außerhalb der bekannten Perzentile"

                            with st.expander(f"{display_name} Vergleich"):
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric(f"Spieler {display_name}", f"{player_value:.2f}".replace(".", ","))
                                with col2:
                                    st.metric(f"Median (50%)", f"{median_value:.2f}".replace(".", ","))
                                with col3:
                                    st.markdown(f'<p style="font-size:25px; color:white;">Einordnung:<br> {player_position_text}</p>', unsafe_allow_html=True)

                                # Boxplot mit Spielerwert markieren
                                fig = create_percentile_curve(stat_values, player_value, xlabel=display_name)
                                st.pyplot(fig)

                    # Anzeige der Vergleiche in 2x2-Matrix
                    def display_comparison_grid():
                        # Definition der Metriken je nach Spiel
                        if chosen_app_id == 730:  # Counter-Strike 2
                            metrics = [
                                ("KD_ratio", "K/D-Ratio", ""),
                                ("accuracy", "Trefferquote", "%"),
                                ("headshot_ratio", "Headshot-Quote", " %"),
                                ("win_ratio", "Siegesquote", "%")
                            ]
                        elif chosen_app_id == 648800:  # Raft
                            metrics = [
                                ("stat_player_deaths", "Tode", ""),
                                ("stat_player_sharkKills", "Getötete Haie", ""),
                                ("stat_player_capturedAnimals", "Eingefangene Tiere", ""),
                                ("stat_player_hookCount", "Hakenwürfe", ""),
                                ("stat_player_excevations_treasure", "Gehobene Schätze", ""),
                                ("stat_player_zipline_distance", "Seilrutschen-Distanz (m)", " m")
                            ]
                        elif chosen_app_id == 222880:  # Insurgency
                            metrics = [
                                ("TotalKills", "Kills im kompetitiven Modus", ""),
                                ("TotalKillsCoop", "Kills im Koop-Modus", ""),
                                ("TotalMVPs", "MVP-Auszeichnungen im kompetitiven Modus", ""),
                                ("TotalMVPsCoop", "MVP-Auszeichnungen im Koop-Modus", ""),
                                ("TotalCaptures", "Eroberten Ziele im kompetitiven Modus", ""),
                                ("TotalCapturesCoop", "Eroberten Ziele im Koop-Modus", "")
                            ]
                        elif chosen_app_id == 221100:  # DayZ
                            metrics = [
                                ("STAT_ACTION_EAT", "Anzahl Essaktionen", ""),
                                ("STAT_ACTION_DRINK", "Anzahl Trinkaktionen", ""),
                                ("STAT_ACTION_COOK_STEAK", "Gekochte Steaks", ""),
                                ("STAT_ACTION_IGNITE_FIRE_MATCHBOX", "Feuer mit Streichhölzern entzündet", ""),
                                ("STAT_ACTION_IGNITE_FIRE_HAND_DRILL", "Feuer mit Handbohrer entzündet", ""),
                                ("STAT_ACTION_EQUIP_GEAR", "Ausrüstung angelegt", ""),
                                ("STAT_ACTION_SHAVE", "Durchgeführte Rasuren", ""),
                                ("STAT_ACTION_GUT_DEER", "Hirsche ausgeweidet", ""),
                                ("STAT_ACTION_APPLY_MEDS_ON_SURVIVOR", "Medikamente bei Überlebenden angewendet", ""),
                                ("STAT_INFECTED_KILL_COUNT", "Infizierte getötet", ""),
                                ("STAT_INFECTED_SOLDIER_KILL_COUNT", "Infizierte Soldaten getötet", ""),
                                ("STAT_INFECTED_HEADSHOT_COUNT", "Infizierte per Kopfschuss getötet", ""),
                                ("STAT_SURVIVOR_KILL_MAX_DIST", "Max. Killdistanz (Überlebende)", ""),
                                ("STAT_SURVIVOR_MELEE_KILL_COUNT", "Nahkampf-Kills (Überlebende)", ""),
                                ("STAT_SURVIVOR_HEADSHOT_COUNT", "Kopfschüsse an Überlebenden", ""),
                                ("STAT_HEADSHOT_COUNT", "Gesamte Kopfschüsse", "")
                            ]
                        else:
                            metrics = []  # Falls kein passendes Spiel gefunden wird

                        # Anzahl der Spalten pro Zeile (hier: 2 pro Zeile)
                        cols_per_row = 2

                        # Iteration über die Metriken in Schritten von cols_per_row
                        for i in range(0, len(metrics), cols_per_row):
                            # Ermitteln des aktuellen Zeilen-Segments und Erstellen nötiger Spaltenzahl
                            row_metrics = metrics[i:i + cols_per_row]
                            columns = st.columns(len(row_metrics))
                            for col, metric in zip(columns, row_metrics):
                                with col:
                                    display_comparison(*metric)


                    # -------------------------------
                    # Haupt-Logik zum Abrufen und Anzeigen der Daten
                    # -------------------------------
                    if user_game_data.get("status") == "success":
                        stats_list = user_game_data.get("stats", [])
                        stats_dict = {stat["name"]: stat["value"] for stat in stats_list}
                        
                        #nur positive Werte, egal welche Daten
                        stats_dict = {key: max(0, value) for key, value in stats_dict.items()}
                        # Debug: Daten checken
                        # st.write("Stats Dict Debug:", stats_dict)

                        if chosen_app_id == 730:  # Counter-Strike 2
                            kills = stats_dict.get("total_kills", 0)
                            deaths = stats_dict.get("total_deaths", 0)
                            shots_fired = stats_dict.get("total_shots_fired", 0)
                            shots_hit = stats_dict.get("total_shots_hit", 0)
                            headshots = stats_dict.get("total_kills_headshot", 0)
                            matches_played = stats_dict.get("total_matches_played", 0)
                            matches_won = stats_dict.get("total_matches_won", 0)

                            # Vergleichswerte für CS2
                            comparison_metrics = {
                                "KD_ratio": kills / deaths if deaths > 0 else np.nan,
                                "accuracy": (shots_hit / shots_fired) * 100 if shots_fired > 0 else np.nan,
                                "headshot_ratio": (headshots / shots_hit) * 100 if shots_hit > 0 else np.nan,
                                "win_ratio": (matches_won / matches_played) * 100 if matches_played > 0 else np.nan
                            }

                        elif chosen_app_id == 648800:  # Raft
                            deaths = stats_dict.get("stat_player_deaths", 0)
                            shark_kills = stats_dict.get("stat_player_sharkKills", 0)
                            captured_animals = stats_dict.get("stat_player_capturedAnimals", 0)
                            hook_count = stats_dict.get("stat_player_hookCount", 0)
                            excevations_treasure = stats_dict.get("stat_player_excevations_treasure", 0)
                            zipline_distance = stats_dict.get("stat_player_zipline_distance", 0)

                            # Vergleichswerte für Raft
                            comparison_metrics = {
                                "stat_player_deaths": deaths,
                                "stat_player_sharkKills": shark_kills,
                                "stat_player_capturedAnimals": captured_animals,
                                "stat_player_hookCount": hook_count,
                                "stat_player_excevations_treasure": excevations_treasure,
                                "stat_player_zipline_distance": zipline_distance
                            }
                        
                        elif chosen_app_id == 222880:  # Insurgency
                            total_kills = stats_dict.get("TotalKills", 0)
                            total_captures = stats_dict.get("TotalCaptures", 0)
                            total_mvps = stats_dict.get("TotalMVPs", 0)
                            total_kills_coop = stats_dict.get("TotalKillsCoop", 0)
                            total_captures_coop = stats_dict.get("TotalCapturesCoop", 0)
                            total_mvps_coop = stats_dict.get("TotalMVPsCoop", 0)

                            # Vergleichswerte für Insurgency
                            comparison_metrics = {
                                "TotalKills": round(total_kills),
                                "TotalCaptures": round(total_captures),
                                "TotalMVPs": round(total_mvps),
                                "TotalKillsCoop": round(total_kills_coop),
                                "TotalCapturesCoop": round(total_captures_coop),
                                "TotalMVPsCoop": round(total_mvps_coop)
                            }
                        
                        elif chosen_app_id == 221100:  # DayZ
                            stat_action_eat = stats_dict.get("STAT_ACTION_EAT", 0)
                            stat_action_drink = stats_dict.get("STAT_ACTION_DRINK", 0)
                            stat_action_cook_steak = stats_dict.get("STAT_ACTION_COOK_STEAK", 0)
                            stat_action_ignite_fire_matchbox = stats_dict.get("STAT_ACTION_IGNITE_FIRE_MATCHBOX", 0)
                            stat_action_ignite_fire_hand_drill = stats_dict.get("STAT_ACTION_IGNITE_FIRE_HAND_DRILL", 0)
                            stat_action_equip_gear = stats_dict.get("STAT_ACTION_EQUIP_GEAR", 0)
                            stat_action_shave = stats_dict.get("STAT_ACTION_SHAVE", 0)
                            stat_action_gut_deer = stats_dict.get("STAT_ACTION_GUT_DEER", 0)
                            stat_action_apply_meds_on_survivor = stats_dict.get("STAT_ACTION_APPLY_MEDS_ON_SURVIVOR", 0)
                            stat_infected_kill_count = stats_dict.get("STAT_INFECTED_KILL_COUNT", 0)
                            stat_infected_soldier_kill_count = stats_dict.get("STAT_INFECTED_SOLDIER_KILL_COUNT", 0)
                            stat_infected_headshot_count = stats_dict.get("STAT_INFECTED_HEADSHOT_COUNT", 0)
                            stat_survivor_kill_max_dist = stats_dict.get("STAT_SURVIVOR_KILL_MAX_DIST", 0)
                            stat_survivor_melee_kill_count = stats_dict.get("STAT_SURVIVOR_MELEE_KILL_COUNT", 0)
                            stat_survivor_headshot_count = stats_dict.get("STAT_SURVIVOR_HEADSHOT_COUNT", 0)
                            stat_headshot_count = stats_dict.get("STAT_HEADSHOT_COUNT", 0)

                            
                            comparison_metrics = {
                                "STAT_ACTION_EAT": round(stat_action_eat),
                                "STAT_ACTION_DRINK": round(stat_action_drink),
                                "STAT_ACTION_COOK_STEAK": round(stat_action_cook_steak),
                                "STAT_ACTION_IGNITE_FIRE_MATCHBOX": round(stat_action_ignite_fire_matchbox),
                                "STAT_ACTION_IGNITE_FIRE_HAND_DRILL": round(stat_action_ignite_fire_hand_drill),
                                "STAT_ACTION_EQUIP_GEAR": round(stat_action_equip_gear),
                                "STAT_ACTION_SHAVE": round(stat_action_shave),
                                "STAT_ACTION_GUT_DEER": round(stat_action_gut_deer),
                                "STAT_ACTION_APPLY_MEDS_ON_SURVIVOR": round(stat_action_apply_meds_on_survivor),
                                "STAT_INFECTED_KILL_COUNT": round(stat_infected_kill_count),
                                "STAT_INFECTED_SOLDIER_KILL_COUNT": round(stat_infected_soldier_kill_count),
                                "STAT_INFECTED_HEADSHOT_COUNT": round(stat_infected_headshot_count),
                                "STAT_SURVIVOR_KILL_MAX_DIST": round(stat_survivor_kill_max_dist, 2),
                                "STAT_SURVIVOR_MELEE_KILL_COUNT": round(stat_survivor_melee_kill_count),
                                "STAT_SURVIVOR_HEADSHOT_COUNT": round(stat_survivor_headshot_count),
                                "STAT_HEADSHOT_COUNT": round(stat_headshot_count)
                            }

                        # Aufruf der Matrix-Anzeige
                        display_comparison_grid()

                    else:
                        st.warning("Fehler beim Abrufen der Spielstatistiken.")
        else:
            st.warning("STEAM ID eingeben!")                
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
# Tab "Freunde Vergleich"
# Freunde-Vergleich
import textwrap

# Funktion für Umbruch der Spielnamen
def wrap_labels(labels, width=10):
    return ['\n'.join(textwrap.wrap(label, width)) for label in labels]

with tabs[3]:
    st.header("\U0001F465 Freunde-Vergleich")

    steam_id_1 = st.text_input(label="STEAM-ID", placeholder="--- Gib hier die erste SteamID64 ein ---", label_visibility="hidden")
    steam_id_2 = st.text_input(label="STEAM-ID", placeholder="--- Gib hier die zweite SteamID64 ein ---", label_visibility="hidden")
    button_compare = st.button("Vergleichen")

    if steam_id_1 and steam_id_2:
        st.write(f"\U0001F4CA **Vergleich von Steam-IDs:** `{steam_id_1}` & `{steam_id_2}`")
        st.write("\U0001F504 **Lade Benutzer- und Spiele-Daten...**")

        with st.spinner("Daten werden geladen..."):
            result_1 = user_owned_games.get_owned_games(API_KEY, steam_id_1)
            result_2 = user_owned_games.get_owned_games(API_KEY, steam_id_2)
            info_result_1 = user_info.get_user_info(API_KEY, steam_id_1)
            info_result_2 = user_info.get_user_info(API_KEY, steam_id_2)

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
                user_game_ids_1 = [game["appid"] for game in games_1]
                user_game_ids_2 = [game["appid"] for game in games_2]
                common_game_ids = set(user_game_ids_1) & set(user_game_ids_2)

                array_games_updated = pd.DataFrame(
                    [row for _, row in array_games.iterrows() if row["App-ID"] in common_game_ids]
                )

                if array_games_updated.empty or "Name" not in array_games_updated.columns:
                    st.warning("Es wurden keine gemeinsamen relevanten Spiele gefunden.")
                else:
                    st.subheader("🎮 **Gemeinsame Spiele mit Spielzeit**")
                    selected_game = st.selectbox("Wähle ein Spiel für weitere Statistiken:", array_games_updated["Name"].tolist())
                    
                    chosen_app_id_comp = array_games_updated.loc[array_games_updated["Name"] == selected_game, "App-ID"].values[0]

                    # Gemeinsame Spiele ermitteln
                    df_1 = pd.DataFrame(games_1)[["appid", "name", "playtime_forever"]].rename(columns={"name": "Name", "playtime_forever": "Spielzeit in Stunden"})
                    df_2 = pd.DataFrame(games_2)[["appid", "name", "playtime_forever"]].rename(columns={"name": "Name", "playtime_forever": "Spielzeit in Stunden"})
                    
                    # Minuten in Stunden umwandeln
                    df_1["Spielzeit in Stunden"] = (df_1["Spielzeit in Stunden"] / 60).round(2)
                    df_2["Spielzeit in Stunden"] = (df_2["Spielzeit in Stunden"] / 60).round(2)
                    
                    # Gemeinsame Spiele filtern
                    common_games = pd.merge(df_1, df_2, on=["appid", "Name"], suffixes=(" Spieler 1", " Spieler 2"))
                    common_games_withplaytime = common_games[(common_games["Spielzeit in Stunden Spieler 1"] > 0) & (common_games["Spielzeit in Stunden Spieler 2"] > 0)]
                    common_games_withplaytime.reset_index(drop=True, inplace=True)
                    if not common_games.empty:
                     # Spalten für Tabelle (links) und Grafik (rechts)
                        col1, col2 = st.columns([1.3, 1.7])  # Verhältnis: 1.5 : 1

                        with col1:  # **Tabelle links**
                            st.dataframe(common_games_withplaytime[["Name", "Spielzeit in Stunden Spieler 1", "Spielzeit in Stunden Spieler 2"]].sort_values(by="Spielzeit in Stunden Spieler 1", ascending=False), hide_index=True, use_container_width=True)

                        with col2:  # **Graphik rechts**
                            # Balkendiagramm mit den Top 5 gemeinsamen Spielen nach Spielzeit, wenn beide Spieler gespielt haben
                            top_5_games = common_games_withplaytime.sort_values(by="Spielzeit in Stunden Spieler 1", ascending=False).head(5)

                            fig, ax = plt.subplots(figsize=(5, 2))  # Kleinere Grafik für Spaltenlayout
                            # Hintergrund entfernen
                            fig.patch.set_visible(False)  # Entfernt gesamten Hintergrund
                            ax.set_facecolor("none")  # Entfernt Achsen-Hintergrund
                            ax.spines["top"].set_visible(False)
                            ax.spines["right"].set_visible(False)
                            ax.spines["left"].set_visible(False)
                            ax.spines["bottom"].set_visible(False)
                                                
                            bar_width = 0.3
                            indices = range(len(top_5_games))
                            ax.bar([i - bar_width/2 for i in indices], top_5_games["Spielzeit in Stunden Spieler 1"], width=bar_width, label="Spieler 1", alpha=0.7)
                            ax.bar([i + bar_width/2 for i in indices], top_5_games["Spielzeit in Stunden Spieler 2"], width=bar_width, label="Spieler 2", alpha=0.7)
                            # Spielnamen mit Zeilenumbruch
                            wrapped_labels = wrap_labels(top_5_games["Name"], width=15)  # Breite des Umbruchs anpassen
                           
                            ax.set_xticks(indices)
                            ax.set_xticklabels(wrapped_labels, rotation=0, ha="center", fontsize=6)
                            ax.set_ylabel("Spielzeit (Stunden)", fontsize=6)
                            ax.tick_params(axis='both',colors="white", labelsize=5)
                            ax.set_title("Top 5 gemeinsame Spiele nach Spielzeit (Spieler 1)", color="white", fontsize=8)
                            ax.legend(fontsize=6)

                            st.pyplot(fig)
                    else:
                        st.write("⚠️ **Keine gemeinsamen Spiele aus der definierten Liste gefunden.**")
    
    
        #Abfrage gemeinsamer Spieldaten und Vergleich
        # Fehlerprüfung für Benutzerinfos
        st.subheader("🔍 **In-Game-Statistiken**")
        
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

        user_game_data_1 = user_game.fetch_in_game_data(API_KEY, steam_id_1,  chosen_app_id_comp)
        user_game_data_2 = user_game.fetch_in_game_data(API_KEY, steam_id_2,  chosen_app_id_comp)
        
         # Prüfen, ob beide Spieler gültige Daten haben
        if user_game_data_1.get("status") == "success" and user_game_data_2.get("status") == "success":
            stats_list_1 = user_game_data_1.get("stats", [])
            stats_list_2 = user_game_data_2.get("stats", [])

            # Relevante Statistiken für die gewählte App-ID aus STAT_MAPPING holen
            relevant_stats = set(STAT_MAPPING.get(str( chosen_app_id_comp), []))

            # Statistiken für beide Spieler filtern
            filtered_stats_1 = {stat["name"]: stat["value"] for stat in stats_list_1 if stat["name"] in relevant_stats}
            filtered_stats_2 = {stat["name"]: stat["value"] for stat in stats_list_2 if stat["name"] in relevant_stats}

            # Nur gemeinsame Statistiken behalten
            common_stat_names = set(filtered_stats_1.keys()) & set(filtered_stats_2.keys())

            if common_stat_names:
                if  chosen_app_id_comp == 730:            
                    with st.expander("Zeige allgemeine Spielstatistiken"):
                        # DataFrame für übersichtliche Anzeige in einer Tabelle erstellen
                        df_stats = pd.DataFrame(
                            {
                                "Statistik": list(common_stat_names),
                                "Spieler 1": [filtered_stats_1[name] for name in common_stat_names],
                                "Spieler 2": [filtered_stats_2[name] for name in common_stat_names],
                            }
                        )
                        #st.write("### Zeige allgemeine Spielstatistiken")
                        #st.dataframe(df_stats)
                        # KD-Ratio berechnen und anzeigen
                        deaths_1 = filtered_stats_1.get("total_deaths", 0)
                        kills_1 = filtered_stats_1.get("total_kills", 0)
                        kd_ratio_1 = kills_1 / deaths_1 if deaths_1 > 0 else float("inf")

                        deaths_2 = filtered_stats_2.get("total_deaths", 0)
                        kills_2 = filtered_stats_2.get("total_kills", 0)
                        kd_ratio_2 = kills_2 / deaths_2 if deaths_2 > 0 else float("inf")

                        # Spielzeit in Stunden umrechnen
                        time_played_hours_1 = filtered_stats_1.get("total_time_played", 0) / 3600
                        time_played_hours_2 = filtered_stats_2.get("total_time_played", 0) / 3600

                        # Weitere relevante Statistiken abrufen
                        total_wins_1 = filtered_stats_1.get("total_wins", 0)
                        total_wins_2 = filtered_stats_2.get("total_wins", 0)

                        total_rounds_1 = filtered_stats_1.get("total_rounds_played", 0)
                        total_rounds_2 = filtered_stats_2.get("total_rounds_played", 0)

                        # Metriken für Spieler 1 und 2 nebeneinander anzeigen
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Abschüsse (Spieler 1)", f"{kills_1:,}".replace(",", "."))
                            st.metric("Tode (Spieler 1)", f"{deaths_1:,}".replace(",", "."))
                            st.metric("KD-Ratio (Spieler 1)", f"{kd_ratio_1:.2f}".replace(".", ","))
                            st.metric("Spielzeit [h] (Spieler 1)", f"{time_played_hours_1:,.0f}".replace(",", "."))
                            st.metric("Siege gesamt (Spieler 1)", f"{total_wins_1:,}".replace(",", "."))
                            st.metric("Gespielte Runden (Spieler 1)", f"{total_rounds_1:,}".replace(",", "."))

                        with col2:
                            st.write("")  # Platzhalter für Abstand
                        
                        with col3:
                            st.metric("Abschüsse (Spieler 2)", f"{kills_2:,}".replace(",", "."))
                            st.metric("Tode (Spieler 2)", f"{deaths_2:,}".replace(",", "."))
                            st.metric("KD-Ratio (Spieler 2)", f"{kd_ratio_2:.2f}".replace(".", ","))
                            st.metric("Spielzeit [h] (Spieler 2)", f"{time_played_hours_2:,.0f}".replace(",", "."))
                            st.metric("Siege gesamt (Spieler 2)", f"{total_wins_2:,}".replace(",", "."))
                            st.metric("Gespielte Runden (Spieler 2)", f"{total_rounds_2:,}".replace(",", "."))
                    
                    with st.expander("Zeige Match-Statistiken"):
                        # Matchdaten für Spieler 1
                        matches_played_1 = filtered_stats_1.get("total_matches_played", 0)
                        matches_won_1 = filtered_stats_1.get("total_matches_won", 0)
                        win_ratio_1 = (matches_won_1 / matches_played_1 * 100) if matches_played_1 > 0 else float("inf")

                        # Matchdaten für Spieler 2
                        matches_played_2 = filtered_stats_2.get("total_matches_played", 0)
                        matches_won_2 = filtered_stats_2.get("total_matches_won", 0)
                        win_ratio_2 = (matches_won_2 / matches_played_2 * 100) if matches_played_2 > 0 else float("inf")

                        # GG-Daten für Spieler 1
                        gg_played_1 = filtered_stats_1.get("total_gg_matches_played", 0)
                        gg_won_1 = filtered_stats_1.get("total_gg_matches_won", 0)
                        gg_ratio_1 = (gg_won_1 / gg_played_1 * 100) if gg_played_1 > 0 else float("inf")

                        # GG-Daten für Spieler 2
                        gg_played_2 = filtered_stats_2.get("total_gg_matches_played", 0)
                        gg_won_2 = filtered_stats_2.get("total_gg_matches_won", 0)
                        gg_ratio_2 = (gg_won_2 / gg_played_2 * 100) if gg_played_2 > 0 else float("inf")

                        # Match-Statistiken für beide Spieler nebeneinander anzeigen
                        st.write("### Vergleich der Match-Statistiken")

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.subheader("Spieler 1")
                            custom_metric("Gespielte Matches", f"{matches_played_1:,}".replace(",", "."))
                            custom_metric("Gewonnene Matches", f"{matches_won_1:,}".replace(",", "."))
                            custom_metric("Siegesquote", f"{win_ratio_1:.1f}".replace(".", ",") + " %")

                            custom_metric("Gespielte GG-Matches", f"{gg_played_1:,}".replace(",", "."))
                            custom_metric("Gewonnene GG-Matches", f"{gg_won_1:,}".replace(",", "."))
                            custom_metric("GG-Siegesquote", f"{gg_ratio_1:.1f}".replace(".", ",") + " %")

                        with col2:
                            st.write("")  # Platzhalter für Abstand

                        with col3:
                            st.subheader("Spieler 2")
                            custom_metric("Gespielte Matches", f"{matches_played_2:,}".replace(",", "."))
                            custom_metric("Gewonnene Matches", f"{matches_won_2:,}".replace(",", "."))
                            custom_metric("Siegesquote", f"{win_ratio_2:.1f}".replace(".", ",") + " %")

                            custom_metric("Gespielte GG-Matches", f"{gg_played_2:,}".replace(",", "."))
                            custom_metric("Gewonnene GG-Matches", f"{gg_won_2:,}".replace(",", "."))
                            custom_metric("GG-Siegesquote", f"{gg_ratio_2:.1f}".replace(".", ",") + " %")

                        # Zusätzlicher Platz durch eine Leerzeile und Padding für bessere Darstellung
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
                        # Schussdaten für Spieler 1
                        shots_fired_1 = filtered_stats_1.get("total_shots_fired", 0)
                        shots_hit_1 = filtered_stats_1.get("total_shots_hit", 0)
                        headshots_1 = filtered_stats_1.get("total_kills_headshot", 0)
                        shots_missed_1 = shots_fired_1 - shots_hit_1  

                        accuracy_1 = (shots_hit_1 / shots_fired_1 * 100) if shots_fired_1 > 0 else 0
                        headshot_ratio_1 = (headshots_1 / shots_hit_1 * 100) if shots_hit_1 > 0 else 0

                        # Schussdaten für Spieler 2
                        shots_fired_2 = filtered_stats_2.get("total_shots_fired", 0)
                        shots_hit_2 = filtered_stats_2.get("total_shots_hit", 0)
                        headshots_2 = filtered_stats_2.get("total_kills_headshot", 0)
                        shots_missed_2 = shots_fired_2 - shots_hit_2  

                        accuracy_2 = (shots_hit_2 / shots_fired_2 * 100) if shots_fired_2 > 0 else 0
                        headshot_ratio_2 = (headshots_2 / shots_hit_2 * 100) if shots_hit_2 > 0 else 0

                        # Anzeige der wichtigsten Schussstatistiken für beide Spieler
                        st.write("### Vergleich der Treffer- und Headshot-Statistiken")

                        col1, col2, col3, col4, col5, col6 = st.columns(6)
                        with col1:
                            st.subheader("Spieler 1")
                            custom_metric("Abgefeuerte Schüsse", f"{shots_fired_1:,}".replace(",", "."))
                            #custom_metric("Treffer", f"{shots_hit_1:,}".replace(",", "."))
                            #custom_metric("Headshots", f"{headshots_1:,}".replace(",", "."))
                            #custom_metric("Treffgenauigkeit", f"{accuracy_1:.1f}".replace(".", ",") + " %")
                            #custom_metric("Headshot-Rate", f"{headshot_ratio_1:.1f}".replace(".", ",") + " %")

                        with col4:
                            st.subheader("Spieler 2")
                            custom_metric("Abgefeuerte Schüsse", f"{shots_fired_2:,}".replace(",", "."))
                            #custom_metric("Treffer", f"{shots_hit_2:,}".replace(",", "."))
                            #custom_metric("Headshots", f"{headshots_2:,}".replace(",", "."))
                            #custom_metric("Treffgenauigkeit", f"{accuracy_2:.1f}".replace(".", ",") + " %")
                            #custom_metric("Headshot-Rate", f"{headshot_ratio_2:.1f}".replace(".", ",") + " %")

                        # Grafiken für beide Spieler nebeneinander
                        col7, col8 = st.columns(2)
                        
                        figsize = (2, 2)  # Einheitliche Diagrammgröße
                        dpi = 20
                        plt.rcParams['figure.facecolor'] = '#0E1117'  # Hintergrundfarbe Schwarz

                        # Spieler 1 - Treffer vs. Verfehlt Diagramm
                        with col7:
                            #st.subheader("Spieler 1 - Trefferverhältnis")
                            labels = ["Treffer", "Verfehlt"]
                            sizes = [shots_hit_1, shots_missed_1]
                            colors = ["#8d2c91", "#68D2FA"]
                            explode = (0.1, 0)

                            fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
                            ax.set_facecolor("#0E1117")
                            ax.pie(
                                sizes,
                                explode=explode,
                                labels=labels,
                                colors=colors,
                                autopct=lambda p: f'{p:.1f}%\n{int(sizes[int(p > 50)]):,.0f}'.replace(',', '.'),
                                startangle=140,
                                textprops={'color': "white", 'fontsize': 6},
                            )
                            ax.axis("equal")  
                            st.pyplot(fig)

                        with col8:
                            #st.subheader("Spieler 2 - Trefferverhältnis")
                            labels_2 = ["Treffer", "Verfehlt"]
                            sizes_2 = [shots_hit_2, shots_missed_2]
                            colors_2 = ["#8d2c91", "#68D2FA"]
                            explode_2 = (0.1, 0)

                            fig2, ax2 = plt.subplots(figsize=figsize, dpi=dpi)
                            ax2.set_facecolor("#0E1117")
                            ax2.pie(
                                sizes_2,
                                explode=explode_2,
                                labels=labels_2,
                                colors=colors_2,
                                autopct=lambda p: f'{p:.1f}%\n{int(sizes_2[int(p > 50)]):,.0f}'.replace(',', '.'),
                                startangle=140,
                                textprops={'color': "white", 'fontsize': 6},
                            )
                            ax2.axis("equal")
                            st.pyplot(fig2)

                        # Headshot-Verteilung für beide Spieler nebeneinander
                        col9, col10 = st.columns(2)

                        with col9:
                            st.subheader("Spieler 1 - Headshot-Rate")
                            headshot_labels = ["Headshots", "Andere Treffer"]
                            headshot_sizes = [headshots_1, max(shots_hit_1 - headshots_1, 0)]
                            headshot_colors = ["#b66bb2", "#d4a3d9"]
                            explode_headshots = (0.1, 0)

                            fig3, ax3 = plt.subplots(figsize=figsize, dpi=dpi)
                            ax3.set_facecolor("#0E1117")
                            ax3.pie(
                                headshot_sizes,
                                explode=explode_headshots,
                                labels=headshot_labels,
                                colors=headshot_colors,
                                autopct=lambda p: f'{p:.1f}%\n{int(headshot_sizes[int(p > 50)]):,.0f}'.replace(',', '.'),
                                startangle=140,
                                textprops={'color': "white", 'fontsize': 6},
                            )
                            ax3.axis("equal")
                            st.pyplot(fig3)

                        with col10:
                            st.subheader("Spieler 2 - Headshot-Rate")
                            headshot_labels_2 = ["Headshots", "Andere Treffer"]
                            headshot_sizes_2 = [headshots_2, max(shots_hit_2 - headshots_2, 0)]
                            headshot_colors_2 = ["#b66bb2", "#d4a3d9"]
                            explode_headshots_2 = (0.1, 0)

                            fig4, ax4 = plt.subplots(figsize=figsize, dpi=dpi)
                            ax4.set_facecolor("#0E1117")
                            ax4.pie(
                                headshot_sizes_2,
                                explode=explode_headshots_2,
                                labels=headshot_labels_2,
                                colors=headshot_colors_2,
                                autopct=lambda p: f'{p:.1f}%\n{int(headshot_sizes_2[int(p > 50)]):,.0f}'.replace(',', '.'),
                                startangle=140,
                                textprops={'color': "white", 'fontsize': 6},
                            )
                            ax4.axis("equal")
                            st.pyplot(fig4)

                        # Abstand zur nächsten Sektion
                        st.markdown(
                            """
                            <style>
                            .st-expander .stContainer {
                                padding-bottom: 20px; 
                            }
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )

                    with st.expander("Waffen-Statistiken"):

                        # Liste aller Waffen
                        weapons = [
                            "ak47", "aug", "awp", "bizon", "deagle", "elite", "famas", "fiveseven", "g3sg1", "galilar",
                            "glock", "hkp2000", "m249", "m4a1", "mac10", "mag7", "mp7", "mp9", "negev", "nova",
                            "p250", "p90", "sawedoff", "scar20", "sg556", "ssg08", "tec9", "ump45", "xm1014"
                        ]

                        # Listen für die Ergebnisse der Spieler
                        weapon_stats_1, weapon_stats_2 = [], []

                        # Daten für beide Spieler berechnen
                        for weapon in weapons:
                            # Spieler 1
                            hits_1 = filtered_stats_1.get(f"total_hits_{weapon}", 0)
                            kills_1 = filtered_stats_1.get(f"total_kills_{weapon}", 0)
                            shots_1 = filtered_stats_1.get(f"total_shots_{weapon}", 1)  # Division durch 0 vermeiden
                            accuracy_1 = hits_1 / shots_1  
                            efficiency_1 = kills_1 / shots_1
                            weapon_stats_1.append([weapon, hits_1, kills_1, shots_1, accuracy_1, efficiency_1])

                            # Spieler 2
                            hits_2 = filtered_stats_2.get(f"total_hits_{weapon}", 0)
                            kills_2 = filtered_stats_2.get(f"total_kills_{weapon}", 0)
                            shots_2 = filtered_stats_2.get(f"total_shots_{weapon}", 1)  # Division durch 0 vermeiden
                            accuracy_2 = hits_2 / shots_2  
                            efficiency_2 = kills_2 / shots_2
                            weapon_stats_2.append([weapon, hits_2, kills_2, shots_2, accuracy_2, efficiency_2])

                        # Nach Efficiency und Accuracy sortieren (hohe Werte zuerst)
                        sorted_weapon_stats_1 = sorted(weapon_stats_1, key=lambda x: (x[5], x[4]), reverse=True)
                        sorted_weapon_stats_2 = sorted(weapon_stats_2, key=lambda x: (x[5], x[4]), reverse=True)

                        # Top 5 Waffen für beide Spieler
                        top_5_weapons_1 = sorted_weapon_stats_1[:5]
                        top_5_weapons_2 = sorted_weapon_stats_2[:5]

                        # In DataFrame umwandeln
                        df_top5_1 = pd.DataFrame(top_5_weapons_1, columns=["Weapon", "Hits", "Kills", "Shots", "Accuracy", "Efficiency"])
                        df_top5_2 = pd.DataFrame(top_5_weapons_2, columns=["Weapon", "Hits", "Kills", "Shots", "Accuracy", "Efficiency"])

                        # Werte formatieren
                        for df in [df_top5_1, df_top5_2]:
                            df["Hits"] = df["Hits"].apply(lambda x: f"{x:,}".replace(",", "."))
                            df["Kills"] = df["Kills"].apply(lambda x: f"{x:,}".replace(",", "."))
                            df["Shots"] = df["Shots"].apply(lambda x: f"{x:,}".replace(",", "."))
                            df["Accuracy"] = df["Accuracy"].apply(lambda x: f"{x * 100:.1f}%")
                            df["Efficiency"] = df["Efficiency"].apply(lambda x: f"{x * 100:.1f}%")

                        # Waffen-Statistiken für beide Spieler nebeneinander anzeigen
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("Spieler 1 - Top 5 Waffen")
                            st.dataframe(df_top5_1, use_container_width=True)

                        with col2:
                            st.subheader("Spieler 2 - Top 5 Waffen")
                            st.dataframe(df_top5_2, use_container_width=True)

                        # Radar Chart (Accuracy & Efficiency) für beide Spieler
                        labels_1 = [w[0] for w in sorted_weapon_stats_1[:10]]  # Top 10 Waffen für Radar Chart
                        accuracy_values_1 = [w[4] for w in sorted_weapon_stats_1[:10]]
                        efficiency_values_1 = [w[5] for w in sorted_weapon_stats_1[:10]]

                        labels_2 = [w[0] for w in sorted_weapon_stats_2[:10]]  
                        accuracy_values_2 = [w[4] for w in sorted_weapon_stats_2[:10]]
                        efficiency_values_2 = [w[5] for w in sorted_weapon_stats_2[:10]]

                        st.write("Accuracy = Hits / Shots")
                        st.write("Efficiency = Kills / Shots")

                        col3, col4 = st.columns(2)
                        with col3:
                            st.subheader("Spieler 1 - Accuracy vs Efficiency")
                            fig1 = go.Figure()
                            fig1.add_trace(go.Scatterpolar(
                                r=accuracy_values_1 + [accuracy_values_1[0]],  
                                theta=labels_1 + [labels_1[0]],
                                fill='toself',
                                name='Accuracy'
                            ))
                            fig1.add_trace(go.Scatterpolar(
                                r=efficiency_values_1 + [efficiency_values_1[0]],  
                                theta=labels_1 + [labels_1[0]],
                                fill='toself',
                                name='Efficiency'
                            ))
                            fig1.update_layout(
                                polar=dict(
                                    radialaxis=dict(visible=True, range=[0, max(max(accuracy_values_1), max(efficiency_values_1))]),
                                ),
                                showlegend=True,
                                autosize=True
                            )
                            st.plotly_chart(fig1, use_container_width=True, key="radar_chart_1")

                        with col4:
                            st.subheader("Spieler 2 - Accuracy vs Efficiency")
                            fig2 = go.Figure()
                            fig2.add_trace(go.Scatterpolar(
                                r=accuracy_values_2 + [accuracy_values_2[0]],  
                                theta=labels_2 + [labels_2[0]],
                                fill='toself',
                                name='Accuracy'
                            ))
                            fig2.add_trace(go.Scatterpolar(
                                r=efficiency_values_2 + [efficiency_values_2[0]],  
                                theta=labels_2 + [labels_2[0]],
                                fill='toself',
                                name='Efficiency'
                            ))
                            fig2.update_layout(
                                polar=dict(
                                    radialaxis=dict(visible=True, range=[0, max(max(accuracy_values_2), max(efficiency_values_2))]),
                                ),
                                showlegend=True,
                                autosize=True
                            )
                            st.plotly_chart(fig2, use_container_width=True, key="radar_chart_2")

                    with st.expander("Sonstige-Statistiken"):
                        # Statistiken für Spieler 1
                        dbombs_1 = filtered_stats_1.get("total_defused_bombs", 0)
                        pbombs_1 = filtered_stats_1.get("total_planted_bombs", 0)
                        hostages_1 = filtered_stats_1.get("total_rescued_hostages", 0)

                        # Statistiken für Spieler 2
                        dbombs_2 = filtered_stats_2.get("total_defused_bombs", 0)
                        pbombs_2 = filtered_stats_2.get("total_planted_bombs", 0)
                        hostages_2 = filtered_stats_2.get("total_rescued_hostages", 0)

                        # Vergleichsanzeige in zwei Spalten
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("Spieler 1")
                            custom_metric("Entschärfte Bomben", f"{dbombs_1:,}".replace(",", "."))
                            custom_metric("Platzierte Bomben", f"{pbombs_1:,}".replace(",", "."))
                            custom_metric("Gerettete Geiseln", f"{hostages_1:,}".replace(",", "."))

                        with col2:
                            st.subheader("Spieler 2")
                            custom_metric("Entschärfte Bomben", f"{dbombs_2:,}".replace(",", "."))
                            custom_metric("Platzierte Bomben", f"{pbombs_2:,}".replace(",", "."))
                            custom_metric("Gerettete Geiseln", f"{hostages_2:,}".replace(",", "."))

                        # Abstand zur nächsten Sektion für bessere Darstellung
                        st.markdown(
                            """
                            <style>
                            .st-expander .stContainer {
                                padding-bottom: 20px; 
                            }
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )

                    with st.expander("Map-Statistik"):

                        # Dictionary mit den richtigen Keys für jede Map
                        map_keys = {
                            "baggage": "total_rounds_map_ar_baggage",
                            "monastery": "total_rounds_map_ar_monastery",
                            "shoots": "total_rounds_map_ar_shoots",
                            "assault": "total_rounds_map_cs_assault",
                            "italy": "total_rounds_map_cs_italy",
                            "militia": "total_rounds_map_cs_militia",
                            "office": "total_rounds_map_cs_office",
                            "aztec": "total_rounds_map_de_aztec",
                            "cbble": "total_rounds_map_de_cbble",
                            "dust": "total_rounds_map_de_dust",
                            "dust2": "total_rounds_map_de_dust2",
                            "inferno": "total_rounds_map_de_inferno",
                            "lake": "total_rounds_map_de_lake",
                            "nuke": "total_rounds_map_de_nuke",
                            "safehouse": "total_rounds_map_de_safehouse",
                            "stmarc": "total_rounds_map_de_stmarc",
                            "sugarcane": "total_rounds_map_de_sugarcane",
                            "train": "total_rounds_map_de_train",
                            "vertigo": "total_rounds_map_de_vertigo"
                        }

                        # Listen für die Ergebnisse beider Spieler
                        map_stats_1, map_stats_2 = [], []

                        for map_name, key in map_keys.items():
                            # Spieler 1
                            rounds_1 = filtered_stats_1.get(key, 0)
                            map_stats_1.append([map_name, rounds_1])

                            # Spieler 2
                            rounds_2 = filtered_stats_2.get(key, 0)
                            map_stats_2.append([map_name, rounds_2])

                        # Sortierung nach gespielten Runden (Spieler 1)
                        sorted_map_stats_1 = sorted(map_stats_1, key=lambda x: x[1], reverse=True)[:10]
                        sorted_map_stats_2 = {m[0]: m[1] for m in map_stats_2}  # Zu Dict für schnelleren Zugriff

                        # Listen für Diagramm-Daten
                        map_names = [x[0] for x in sorted_map_stats_1]
                        rounds_played_1 = [x[1] for x in sorted_map_stats_1]
                        rounds_played_2 = [sorted_map_stats_2.get(map_name, 0) for map_name in map_names]  # Entsprechende Werte für Spieler 2 holen

                        # Matplotlib Diagramm erstellen
                        fig, ax = plt.subplots(figsize=(3, 2))

                        # Hintergrundfarbe setzen
                        fig.patch.set_facecolor("#0E1117")
                        ax.set_facecolor("#0E1117")

                        # Breite der Balken
                        bar_width = 0.4
                        fontsize = 4
                        indices = np.arange(len(map_names))  # Positionen auf der Y-Achse

                        # Balkendiagramm für beide Spieler erstellen
                        bars1 = ax.barh(indices - bar_width/2, rounds_played_1, bar_width, label="Spieler 1", color="#8d2c91")
                        bars2 = ax.barh(indices + bar_width/2, rounds_played_2, bar_width, label="Spieler 2", color="#68D2FA")

                        # X-Achse erweitern, damit die Zahlen weiter rechts stehen
                        max_value = max(max(rounds_played_1), max(rounds_played_2)) if rounds_played_1 or rounds_played_2 else 1
                        ax.set_xlim(0, max_value * 1.10)  # 10% extra Platz auf der X-Achse

                        # Werte auf die Balken schreiben
                        for bar, value in zip(bars1, rounds_played_1):
                            ax.text(bar.get_width() + (max_value * 0.02), bar.get_y() + bar.get_height() / 2,
                                    f"{value:,}".replace(",", "."), va="center", ha="left", color="white", fontsize=fontsize)

                        for bar, value in zip(bars2, rounds_played_2):
                            ax.text(bar.get_width() + (max_value * 0.02), bar.get_y() + bar.get_height() / 2,
                                    f"{value:,}".replace(",", "."), va="center", ha="left", color="white", fontsize=fontsize)

                        # Achsenbeschriftungen und Titel
                        ax.set_xlabel("Anzahl der gespielten Runden", color="white", fontsize=6)
                        ax.set_title("Top 10 Maps nach Anzahl der gespielten Runden", color="white", fontsize=6)
                        # Y-Achse mit Map-Namen setzen
                        ax.set_yticks(indices)
                        ax.set_yticklabels(map_names, color="white", fontsize=6)
                        # Achsenwerte in Weiß setzen
                        ax.tick_params(axis="x", colors="white", labelsize=fontsize)
                        ax.tick_params(axis="y", colors="white", labelsize=fontsize)
                        # Achsen invertieren für bessere Lesbarkeit
                        ax.invert_yaxis()
                        # X-Achse formatieren
                        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
                        # Rahmen um das Diagramm entfernen
                        ax.spines["top"].set_visible(False)
                        ax.spines["right"].set_visible(False)
                        ax.spines["left"].set_visible(False)
                        ax.spines["bottom"].set_visible(False)
                        # Legende in der oberen rechten Ecke
                        ax.legend(loc="center right", facecolor="#0E1117", edgecolor="white", fontsize=fontsize)
                        st.pyplot(fig)

                elif  chosen_app_id_comp == 648800: #Raft
                                        
                    fontsize = 6
                    with st.expander("Dunkle Statistik"):

                        # Todeszahlen für beide Spieler abrufen
                        deaths_1 = filtered_stats_1.get("stat_player_deaths", 0)
                        deaths_2 = filtered_stats_2.get("stat_player_deaths", 0)

                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("Spieler 1")
                            custom_metric("Tode", f"{deaths_1:,}".replace(",", "."))

                        with col2:
                            st.subheader("Spieler 2")
                            custom_metric("Tode", f"{deaths_2:,}".replace(",", "."))

                    # =======================
                    # Tier-Statistiken für beide Spieler
                    # =======================

                    with st.expander("Statistiken Getötete Tiere"):

                        # Tier-Statistiken für Spieler 1
                        animal_kills_1 = {
                            "Haie": filtered_stats_1.get("stat_player_sharkKills", 0),
                            "Vögel": filtered_stats_1.get("stat_player_birdKills", 0),
                            "Kugelfische": filtered_stats_1.get("stat_player_pufferKills", 0),
                            "Steinwurf-Vögel": filtered_stats_1.get("stat_player_stoneBirdKills", 0),
                            "Ratten": filtered_stats_1.get("stat_player_ratKills", 0),
                            "Bären": filtered_stats_1.get("stat_player_bearKills", 0),
                            "Roboter": filtered_stats_1.get("stat_player_botKills", 0),
                            "Anglerfische": filtered_stats_1.get("stat_player_anglerFishKills", 0),
                            "Wildschweine": filtered_stats_1.get("stat_player_boarKills", 0),
                        }

                        # Tier-Statistiken für Spieler 2
                        animal_kills_2 = {
                            "Haie": filtered_stats_2.get("stat_player_sharkKills", 0),
                            "Vögel": filtered_stats_2.get("stat_player_birdKills", 0),
                            "Kugelfische": filtered_stats_2.get("stat_player_pufferKills", 0),
                            "Steinwurf-Vögel": filtered_stats_2.get("stat_player_stoneBirdKills", 0),
                            "Ratten": filtered_stats_2.get("stat_player_ratKills", 0),
                            "Bären": filtered_stats_2.get("stat_player_bearKills", 0),
                            "Roboter": filtered_stats_2.get("stat_player_botKills", 0),
                            "Anglerfische": filtered_stats_2.get("stat_player_anglerFishKills", 0),
                            "Wildschweine": filtered_stats_2.get("stat_player_boarKills", 0),
                        }

                        # Daten sortieren (nach den höchsten Kills für Spieler 1)
                        sorted_animals = sorted(animal_kills_1.keys(), key=lambda x: animal_kills_1[x], reverse=True)

                        # DataFrame erstellen
                        df_animals = pd.DataFrame({
                            "Tierart": sorted_animals,
                            "Spieler 1": [f"{animal_kills_1[animal]:,}".replace(",", ".") for animal in sorted_animals],
                            "Spieler 2": [f"{animal_kills_2[animal]:,}".replace(",", ".") for animal in sorted_animals]
                        })

                        # DataFrame anzeigen
                        st.dataframe(df_animals, hide_index=True, use_container_width=True)

                        # Balkendiagramm für Vergleich der Tier-Statistiken
                        col5, col6 = st.columns([3, 2])  # Größere linke Spalte für Diagramm
                        with col5:
                            st.subheader("Tier-Statistik Vergleich")

                            # Diagrammdaten vorbereiten
                            animal_labels = sorted_animals
                            kills_1 = [animal_kills_1[animal] for animal in sorted_animals]
                            kills_2 = [animal_kills_2[animal] for animal in sorted_animals]

                            # Matplotlib Diagramm erstellen
                            fig, ax = plt.subplots(figsize=(3, 4))

                            # Hintergrundfarben setzen
                            fig.patch.set_facecolor("#0E1117")
                            ax.set_facecolor("#0E1117")

                            # Balkendiagramm mit zwei Balken pro Tierart (Spieler 1 & 2)
                            bar_width = 0.3
                            indices = np.arange(len(animal_labels))

                            bars1 = ax.barh(indices - bar_width/2, kills_1, bar_width, label="Spieler 1", color="#8d2c91")
                            bars2 = ax.barh(indices + bar_width/2, kills_2, bar_width, label="Spieler 2", color="#68D2FA")

                            # Achsen & Titel anpassen
                            ax.set_xlabel("Anzahl Kills", color="white", fontsize=fontsize)
                            #ax.set_ylabel("Tierart", color="white", fontsize=fontsize)
                            ax.set_title("Getötete Tiere (Spieler 1 vs. Spieler 2)", color="white", fontsize=fontsize)

                            # Achsenbeschriftungen kleiner setzen
                            ax.set_yticks(indices)
                            ax.set_yticklabels(animal_labels, color="white", fontsize=fontsize)
                            ax.tick_params(axis="x", colors="white", labelsize=fontsize)
                            ax.tick_params(axis="y", colors="white", labelsize=fontsize)

                            # Werte auf Balken schreiben
                            for bar, value in zip(bars1, kills_1):
                                ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                                        f"{value:,}".replace(",", "."), va="center", ha="left", color="white", fontsize=fontsize)

                            for bar, value in zip(bars2, kills_2):
                                ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                                        f"{value:,}".replace(",", "."), va="center", ha="left", color="white", fontsize=fontsize)

                            # Y-Achse invertieren für bessere Lesbarkeit
                            ax.invert_yaxis()

                            # Legende mit kleinerer Schrift verschieben
                            ax.legend(loc="center right", bbox_to_anchor=(1, 0.5), facecolor="#0E1117", edgecolor="white", fontsize=fontsize, labelcolor="white")

                            # Diagramm in Streamlit anzeigen
                            st.pyplot(fig)

                        # Weitere Tier-Statistiken (Bienen & gefangene Tiere)
                        with col6:
                            st.subheader("Sonstige Statistiken")

                            # Daten abrufen
                            bees_1 = filtered_stats_1.get("stat_player_captures_bee", 0)
                            bees_2 = filtered_stats_2.get("stat_player_captures_bee", 0)

                            animals_1 = filtered_stats_1.get("stat_player_capturedAnimals", 0)
                            animals_2 = filtered_stats_2.get("stat_player_capturedAnimals", 0)

                            # Falls `animals` ein Tuple ist, nur den ersten Wert nehmen
                            if isinstance(animals_1, tuple):
                                animals_1 = animals_1[0]
                            if isinstance(animals_2, tuple):
                                animals_2 = animals_2[0]

                            # DataFrame erstellen (ohne Index-Spalte)
                            df_stats = pd.DataFrame({
                                "Statistik": ["Bienenschwärme", "Gefangene Tiere"],
                                "Spieler 1": [f"{bees_1:,}".replace(",", "."), f"{animals_1:,}".replace(",", ".")],
                                "Spieler 2": [f"{bees_2:,}".replace(",", "."), f"{animals_2:,}".replace(",", ".")]
                            })

                            # DataFrame anzeigen (ohne Index)
                            st.dataframe(df_stats, hide_index=True, use_container_width=True)

                        # Abstand für saubere Darstellung
                        st.markdown("<br>", unsafe_allow_html=True)

                    with st.expander("Diverse Statistiken"):
                        # Daten für Spieler 1
                        stats_1 = {
                            "Gespielte Noten mit Musikinstrumenten": filtered_stats_1.get("stat_player_instrumentNotes_played", 0),
                            "Abgefeuerte Feuerwerke": filtered_stats_1.get("stat_player_fireworks_launched", 0),
                            "Ausgegrabene Schätze": filtered_stats_1.get("stat_player_excevations_treasure", 0),
                            "Ausgegebene Tokens auf Tangaroa": filtered_stats_1.get("stat_player_token_spend_tangaroa", 0),
                            "Bemalte Objekte": filtered_stats_1.get("stat_build_paintCount", 0),
                            "Entfernte Strukturen": filtered_stats_1.get("stat_build_removeCount", 0),
                            "Verwendung des Hakens": filtered_stats_1.get("stat_player_hookCount", 0),
                            "Gebaute Fundamente": filtered_stats_1.get("stat_build_foundationCount", 0),
                        }

                        # Daten für Spieler 2
                        stats_2 = {
                            "Gespielte Noten mit Musikinstrumenten": filtered_stats_2.get("stat_player_instrumentNotes_played", 0),
                            "Abgefeuerte Feuerwerke": filtered_stats_2.get("stat_player_fireworks_launched", 0),
                            "Ausgegrabene Schätze": filtered_stats_2.get("stat_player_excevations_treasure", 0),
                            "Ausgegebene Tokens auf Tangaroa": filtered_stats_2.get("stat_player_token_spend_tangaroa", 0),
                            "Bemalte Objekte": filtered_stats_2.get("stat_build_paintCount", 0),
                            "Entfernte Strukturen": filtered_stats_2.get("stat_build_removeCount", 0),
                            "Verwendung des Hakens": filtered_stats_2.get("stat_player_hookCount", 0),
                            "Gebaute Fundamente": filtered_stats_2.get("stat_build_foundationCount", 0),
                        }

                        # DataFrame erstellen
                        df_diverse = pd.DataFrame({
                            "Statistik": stats_1.keys(),
                            "Spieler 1": [f"{v:,}".replace(",", ".") for v in stats_1.values()],
                            "Spieler 2": [f"{v:,}".replace(",", ".") for v in stats_2.values()]
                        })

                        # DataFrame anzeigen
                        st.dataframe(df_diverse, hide_index=True, use_container_width=True)

                    # ==========================
                    # Seilrutschen-Statistiken
                    # ==========================

                    with st.expander("Seilrutschen-Statistiken"):
                        # Daten für Spieler 1
                        zipline_stats_1 = {
                            "Zurückgelegte Distanz Seilrutsche [m]": filtered_stats_1.get("stat_player_zipline_distance", 0),
                            "Maximale Distanz Seilrutsche [m]": filtered_stats_1.get("stat_player_zipline_distanceOneGo", 0),
                        }

                        # Daten für Spieler 2
                        zipline_stats_2 = {
                            "Zurückgelegte Distanz Seilrutsche [m]": filtered_stats_2.get("stat_player_zipline_distance", 0),
                            "Maximale Distanz Seilrutsche [m]": filtered_stats_2.get("stat_player_zipline_distanceOneGo", 0),
                        }

                        # DataFrame erstellen
                        df_zipline = pd.DataFrame({
                            "Statistik": zipline_stats_1.keys(),
                            "Spieler 1": [f"{v:,}".replace(",", ".") for v in zipline_stats_1.values()],
                            "Spieler 2": [f"{v:,}".replace(",", ".") for v in zipline_stats_2.values()]
                        })

                        # DataFrame anzeigen
                        st.dataframe(df_zipline, hide_index=True, use_container_width=True)

                elif chosen_app_id_comp == 221100: #DayZ

                    # ==========================
                    # Nahrungs-Statistiken
                    # ==========================

                    with st.expander("Nahrungs-Statistiken"):
                        # Daten für Spieler 1
                        food_stats_1 = {
                            "Aktionen, bei denen Nahrung gegessen wurde": filtered_stats_1.get("STAT_ACTION_EAT", 0),
                            "Aktionen, bei denen Wasser oder andere Flüssigkeiten getrunken wurden": filtered_stats_1.get("STAT_ACTION_DRINK", 0),
                            "Anzahl der gekochten Steaks": filtered_stats_1.get("STAT_ACTION_COOK_STEAK", 0),
                        }

                        # Daten für Spieler 2
                        food_stats_2 = {
                            "Aktionen, bei denen Nahrung gegessen wurde": filtered_stats_2.get("STAT_ACTION_EAT", 0),
                            "Aktionen, bei denen Wasser oder andere Flüssigkeiten getrunken wurden": filtered_stats_2.get("STAT_ACTION_DRINK", 0),
                            "Anzahl der gekochten Steaks": filtered_stats_2.get("STAT_ACTION_COOK_STEAK", 0),
                        }

                        # DataFrame erstellen
                        df_food = pd.DataFrame({
                            "Statistik": food_stats_1.keys(),
                            "Spieler 1": [f"{v:,}".replace(",", ".") for v in food_stats_1.values()],
                            "Spieler 2": [f"{v:,}".replace(",", ".") for v in food_stats_2.values()]
                        })

                        # DataFrame anzeigen
                        st.dataframe(df_food, hide_index=True, use_container_width=True)

                    # ==========================
                    # Praktische-Statistiken
                    # ==========================

                    with st.expander("Praktische-Statistiken"):
                        # Daten für Spieler 1
                        practical_stats_1 = {
                            "Anzahl der entzündeten Feuer mit Streichhölzern": filtered_stats_1.get("STAT_ACTION_IGNITE_FIRE_MATCHBOX", 0),
                            "Anzahl der entzündeten Feuer mit einem Handbohrer": filtered_stats_1.get("STAT_ACTION_IGNITE_FIRE_HAND_DRILL", 0),
                            "Anzahl der Aktionen, bei denen Ausrüstung angelegt wurde": filtered_stats_1.get("STAT_ACTION_EQUIP_GEAR", 0),
                            "Anzahl der durchgeführten Rasuren": filtered_stats_1.get("STAT_ACTION_SHAVE", 0),
                            "Anzahl der ausgeweideten Hirsche": filtered_stats_1.get("STAT_ACTION_GUT_DEER", 0),
                        }

                        # Daten für Spieler 2
                        practical_stats_2 = {
                            "Anzahl der entzündeten Feuer mit Streichhölzern": filtered_stats_2.get("STAT_ACTION_IGNITE_FIRE_MATCHBOX", 0),
                            "Anzahl der entzündeten Feuer mit einem Handbohrer": filtered_stats_2.get("STAT_ACTION_IGNITE_FIRE_HAND_DRILL", 0),
                            "Anzahl der Aktionen, bei denen Ausrüstung angelegt wurde": filtered_stats_2.get("STAT_ACTION_EQUIP_GEAR", 0),
                            "Anzahl der durchgeführten Rasuren": filtered_stats_2.get("STAT_ACTION_SHAVE", 0),
                            "Anzahl der ausgeweideten Hirsche": filtered_stats_2.get("STAT_ACTION_GUT_DEER", 0),
                        }

                        # DataFrame erstellen
                        df_practical = pd.DataFrame({
                            "Statistik": practical_stats_1.keys(),
                            "Spieler 1": [f"{v:,}".replace(",", ".") for v in practical_stats_1.values()],
                            "Spieler 2": [f"{v:,}".replace(",", ".") for v in practical_stats_2.values()]
                        })

                        # DataFrame anzeigen
                        st.dataframe(df_practical, hide_index=True, use_container_width=True)

                    # ==========================
                    # Überlebens-Statistiken
                    # ==========================

                    with st.expander("Überlebens-Statistiken"):
                        # Daten für Spieler 1
                        survival_stats_1 = {
                            "Anzahl der Anwendungen von Medikamenten auf andere Überlebende": filtered_stats_1.get("STAT_ACTION_APPLY_MEDS_ON_SURVIVOR", 0),
                            "Maximale Distanz, aus der ein Überlebender getötet wurde": filtered_stats_1.get("STAT_SURVIVOR_KILL_MAX_DIST", 0),
                            "Anzahl der getöteten Infizierten": filtered_stats_1.get("STAT_INFECTED_KILL_COUNT", 0),
                            "Anzahl der getöteten infizierten Soldaten": filtered_stats_1.get("STAT_INFECTED_SOLDIER_KILL_COUNT", 0),
                            "Anzahl der getöteten Überlebenden mit Nahkampfwaffen": filtered_stats_1.get("STAT_SURVIVOR_MELEE_KILL_COUNT", 0),
                            "Anzahl der Kopfschüsse auf Infizierte": filtered_stats_1.get("STAT_INFECTED_HEADSHOT_COUNT", 0),
                            "Anzahl der Kopfschüsse auf Überlebende": filtered_stats_1.get("STAT_SURVIVOR_HEADSHOT_COUNT", 0),
                            "Gesamtanzahl aller Kopfschüsse": filtered_stats_1.get("STAT_HEADSHOT_COUNT", 0),
                        }

                        # Daten für Spieler 2
                        survival_stats_2 = {
                            "Anzahl der Anwendungen von Medikamenten auf andere Überlebende": filtered_stats_2.get("STAT_ACTION_APPLY_MEDS_ON_SURVIVOR", 0),
                            "Maximale Distanz, aus der ein Überlebender getötet wurde": filtered_stats_2.get("STAT_SURVIVOR_KILL_MAX_DIST", 0),
                            "Anzahl der getöteten Infizierten": filtered_stats_2.get("STAT_INFECTED_KILL_COUNT", 0),
                            "Anzahl der getöteten infizierten Soldaten": filtered_stats_2.get("STAT_INFECTED_SOLDIER_KILL_COUNT", 0),
                            "Anzahl der getöteten Überlebenden mit Nahkampfwaffen": filtered_stats_2.get("STAT_SURVIVOR_MELEE_KILL_COUNT", 0),
                            "Anzahl der Kopfschüsse auf Infizierte": filtered_stats_2.get("STAT_INFECTED_HEADSHOT_COUNT", 0),
                            "Anzahl der Kopfschüsse auf Überlebende": filtered_stats_2.get("STAT_SURVIVOR_HEADSHOT_COUNT", 0),
                            "Gesamtanzahl aller Kopfschüsse": filtered_stats_2.get("STAT_HEADSHOT_COUNT", 0),
                        }

                        # DataFrame erstellen
                        df_survival = pd.DataFrame({
                            "Statistik": survival_stats_1.keys(),
                            "Spieler 1": [f"{v:,}".replace(",", ".") for v in survival_stats_1.values()],
                            "Spieler 2": [f"{v:,}".replace(",", ".") for v in survival_stats_2.values()]
                        })

                        # DataFrame anzeigen
                        st.dataframe(df_survival, hide_index=True, use_container_width=True)
     
                elif chosen_app_id_comp == 222880: #Insurgency
                    # Key-Value-Format ausgeben
                    st.write("**Statistiken**")
                    # ==========================
                    # Kompetitiver Modus - Statistiken

                    with st.expander("Kompetitiver Modus - Statistiken"):
                        # Daten für Spieler 1
                        comp_stats_1 = {
                            "Gesamtanzahl der Kills": filtered_stats_1.get("TotalKills", 0),
                            "Gesamtanzahl der eroberten Ziele": filtered_stats_1.get("TotalCaptures", 0),
                            "Gesamtanzahl der MVP-Auszeichnungen": filtered_stats_1.get("TotalMVPs", 0),
                            "Gesamtanzahl der heldenhaften Eroberungen": filtered_stats_1.get("TotalHeroCaptures", 0),
                        }

                        # Daten für Spieler 2
                        comp_stats_2 = {
                            "Gesamtanzahl der Kills": filtered_stats_2.get("TotalKills", 0),
                            "Gesamtanzahl der eroberten Ziele": filtered_stats_2.get("TotalCaptures", 0),
                            "Gesamtanzahl der MVP-Auszeichnungen": filtered_stats_2.get("TotalMVPs", 0),
                            "Gesamtanzahl der heldenhaften Eroberungen": filtered_stats_2.get("TotalHeroCaptures", 0),
                        }

                        # DataFrame erstellen
                        df_comp = pd.DataFrame({
                            "Statistik": comp_stats_1.keys(),
                            "Spieler 1": [f"{v:,}".replace(",", ".") for v in comp_stats_1.values()],
                            "Spieler 2": [f"{v:,}".replace(",", ".") for v in comp_stats_2.values()]
                        })

                        # DataFrame anzeigen
                        st.dataframe(df_comp, hide_index=True, use_container_width=True)

                    # ==========================
                    # Koop-Modus - Statistiken

                    with st.expander("Koop-Modus - Statistiken"):
                        # Daten für Spieler 1
                        coop_stats_1 = {
                            "Gesamtanzahl der Kills": filtered_stats_1.get("TotalKillsCoop", 0),
                            "Gesamtanzahl der eroberten Ziele": filtered_stats_1.get("TotalCapturesCoop", 0),
                            "Gesamtanzahl der MVP-Auszeichnungen": filtered_stats_1.get("TotalMVPsCoop", 0),
                            "Gesamtanzahl der heldenhaften Eroberungen": filtered_stats_1.get("TotalHeroCapturesCoop", 0),
                        }

                        # Daten für Spieler 2
                        coop_stats_2 = {
                            "Gesamtanzahl der Kills": filtered_stats_2.get("TotalKillsCoop", 0),
                            "Gesamtanzahl der eroberten Ziele": filtered_stats_2.get("TotalCapturesCoop", 0),
                            "Gesamtanzahl der MVP-Auszeichnungen": filtered_stats_2.get("TotalMVPsCoop", 0),
                            "Gesamtanzahl der heldenhaften Eroberungen": filtered_stats_2.get("TotalHeroCapturesCoop", 0),
                        }

                        # DataFrame erstellen
                        df_coop = pd.DataFrame({
                            "Statistik": coop_stats_1.keys(),
                            "Spieler 1": [f"{v:,}".replace(",", ".") for v in coop_stats_1.values()],
                            "Spieler 2": [f"{v:,}".replace(",", ".") for v in coop_stats_2.values()]
                        })

                        # DataFrame anzeigen
                        st.dataframe(df_coop, hide_index=True, use_container_width=True)

                    # ==========================
                    # Gesamt - Statistiken

                    with st.expander("Gesamt - Statistiken"):
                        # Daten für Spieler 1
                        all_stats_1 = {
                            "Gesamtanzahl der Kills": filtered_stats_1.get("TotalKillsAll", 0),
                            "Gesamtanzahl der eroberten Ziele": filtered_stats_1.get("TotalCapturesAll", 0),
                            "Gesamtanzahl der MVP-Auszeichnungen": filtered_stats_1.get("TotalMVPsAll", 0),
                            "Gesamtanzahl der heldenhaften Eroberungen": filtered_stats_1.get("TotalHeroCapturesAll", 0),
                        }

                        # Daten für Spieler 2
                        all_stats_2 = {
                            "Gesamtanzahl der Kills": filtered_stats_2.get("TotalKillsAll", 0),
                            "Gesamtanzahl der eroberten Ziele": filtered_stats_2.get("TotalCapturesAll", 0),
                            "Gesamtanzahl der MVP-Auszeichnungen": filtered_stats_2.get("TotalMVPsAll", 0),
                            "Gesamtanzahl der heldenhaften Eroberungen": filtered_stats_2.get("TotalHeroCapturesAll", 0),
                        }

                        # DataFrame erstellen
                        df_all = pd.DataFrame({
                            "Statistik": all_stats_1.keys(),
                            "Spieler 1": [f"{v:,}".replace(",", ".") for v in all_stats_1.values()],
                            "Spieler 2": [f"{v:,}".replace(",", ".") for v in all_stats_2.values()]
                        })

                        # DataFrame anzeigen
                        st.dataframe(df_all, hide_index=True, use_container_width=True)
                else:
                    st.warning("Für diese App-ID sind entweder keine relevanten Statistiken definiert oder es liegen keine Daten vor.")

            else:
                st.warning("Keine gemeinsamen Statistiken gefunden.")
        else:
            st.error("Fehler beim Abrufen der Daten für einen oder beide Spieler.")

    else:
        st.write("⚠️ **Beide STEAM IDs müssen eingetragen sein**")
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
# Tab "Spiel Empfehlungen"
with tabs[4]:
    st.header("Finde neue Mitspieler und neue Spiele")

    # Cluster CSV-Dateien
    df_clustered_players = pd.read_csv("clustered_players.csv")
    df_final_cluster = pd.read_csv("final_cluster.csv")

    # Genre Datei
    df_genres = pd.read_csv("steam_game_genres_normalized.csv")

    # IDF Datei
    genre_idf = pd.read_csv("genre_idf.csv")
    
    # user_data
    # steam_id ist oben definiert
    if bool_id:

        # Spielerdaten für Clusterzuordnung vorbereiten
        user_data = df_games_cluster.rename(
        columns={"AppID": "appid", "Name": "name", "Playtime (Minutes)": "playtime_forever"}
        )

        # Nur Daten verwenden, für die es auch Genres gibt
        genres_clean = df_genres.dropna(subset=['genres'])
        valid_appids = genres_clean['appid'].unique()
        ud_clean = user_data[user_data['appid'].isin(valid_appids)]

        # genres mergen
        ud_genres = ud_clean.merge(genres_clean, on="appid")
        ud_genres["genres"] = ud_genres["genres"].str.split(",")  # Split Genres
        ud_genres = ud_genres.explode("genres")  # Explode Genres
        ud_genres["genres"] = ud_genres["genres"].str.strip()  # Strip Whitespaces

        # Spielzeit pro Genre
        ud_tf = ud_genres.groupby(["genres"])["playtime_forever"].sum().reset_index()

        # Gesamtspielzeit
        total_playtime = ud_clean["playtime_forever"].sum()

        # Relative TF berechnen (Spielzeit für ein Genre relativ zur gesamten Spielzeit des Spielers)
        ud_tf["TF_relative"] = ud_tf["playtime_forever"] / total_playtime

        # Mit IDF-Werten verknüpfen
        ud_tf = ud_tf.merge(genre_idf, left_on="genres", right_on="Genre", how="left")

        # TF-IDF berechnen
        ud_tf["TF-IDF"] = ud_tf["TF_relative"] * ud_tf["IDF_Playtime"]

        # Unnötige Spalten entfernen
        ud_tf.drop(columns=["playtime_forever", "IDF_Playtime", "Genre"], inplace=True)

        # Cluster zuordnen
        # Relevante Spalten (Genres + Cluster-ID)
        genre_columns = df_final_cluster.columns[1:-1]  # Alle Spalten außer steam_64_id und Cluster
        df_cluster_means = df_final_cluster.groupby("Cluster")[genre_columns].mean()  # Mittelwerte pro Cluster

        # Nutzer-Genre-Daten (aus ud_tf) -> nur "genres" & "TF-IDF"
        user_genre_data = ud_tf.set_index("genres")["TF-IDF"]

        # Ähnlichkeit über euklidische Distanz berechnen
        cluster_distances = {}

        for cluster_id, cluster_row in df_cluster_means.iterrows():
            cluster_vector = cluster_row[genre_columns]  # Cluster-Genres
            user_vector = user_genre_data.reindex(cluster_vector.index).fillna(0)  # Nutzer-Werte, fehlende mit 0

            # Berechne die euklidische Distanz (kleiner = besser)
            distance = euclidean(user_vector, cluster_vector)
            cluster_distances[cluster_id] = distance

        # Bestes Cluster auswählen (nächstgelegenes Cluster)
        best_cluster = min(cluster_distances, key=cluster_distances.get)

        # Ausgabe des zugewiesenen Clusters
        # st.write(f"Spieler wurde Cluster **{best_cluster}** zugeordnet.")

#-----------------------------------------------------------------------------------------------------------------
        # ähnlichste Mitspieler finden
        # Spieler aus dem gleichen Cluster filtern
        player_cluster = df_clustered_players[df_clustered_players["Cluster"] == best_cluster]
        cluster_players = player_cluster["steam_64_id"].unique() 
        #st.write(f"Spieler im Cluster {best_cluster}: {len(cluster_players)}")

        import requests

        def get_friends_list(api_key, steam_id):
            url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={api_key}&steamid={steam_id}&relationship=friend"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if "friendslist" in data:
                    return {friend["steamid"] for friend in data["friendslist"]["friends"]}
            
            return set()  # Falls kein Ergebnis oder Fehler, gib leere Menge zurück

        player_distances = []


        # Berechne euklidische Distanz für jeden Spieler im Cluster
        for player_id in cluster_players:  
            player_vector = df_final_cluster[df_final_cluster["steam_64_id"] == player_id][genre_columns].values.flatten()
            
            # Falls kein Genre-Vektor für diesen Spieler existiert, überspringen
            if player_vector.size == 0:
                continue

            # Euklidische Distanz berechnen
            distance = euclidean(user_vector, player_vector)
            player_distances.append((player_id, distance))


        # Nach Distanz sortieren (niedrigste zuerst) und die Top 10 auswählen
        top_10_players = sorted(player_distances, key=lambda x: x[1])[:10]

        # Freundesliste abrufen
        friend_list = get_friends_list(API_KEY, steam_id)

        # Spieler filtern, die NICHT in der Freundesliste sind
        # Sicherstellen, dass alle Steam-IDs Strings sind und bereinigt werden
        filtered_players = [player for player in top_10_players if str(int(player[0])) not in friend_list and str(int(player[0])) != steam_id]

        # Nur die besten 10 Spieler aus der gefilterten Liste auswählen
        filtered_players = filtered_players[:10]

        if filtered_players:  # Falls es mindestens einen Spieler gibt
            # Ausgabe Mitspielerempfehlung
            # API-Aufruf für Steam-Infos
            def get_steam_info(player_id):
                return user_info.get_user_info(API_KEY, player_id)  # Holt die Steam-Infos

            # Ausgabe: Ähnliche Spieler anzeigen
            st.subheader("Diese Spieler zocken ähnliche Games wie du. Ihr könntet Freunde sein ( ◑‿◑)ɔ┏🍟--🍔┑٩(^◡^ )")
            st.write("")
            st.write("---")

            for i, (player_id, distance) in enumerate(filtered_players):
                if player_id == steam_id:
                    continue

                player_info = get_steam_info(player_id)  # Holt Spielerinfos

                if "personaname" in player_info:
                    col1, col2 = st.columns([3, 3])  # Spalte 1 für Text (3x so groß), Spalte 2 für Avatar

                    with col1:
                        st.write(f"**Ähnlichkeitsrang:** {i + 1}")
                        st.write(f"**Benutzername:** {player_info['personaname']}")
                        st.write(f"**Steam-ID:** {player_id}")

                    with col2:
                        st.markdown(
                            f"""
                            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                                <img src="{player_info['avatarfull']}" alt="Avatar" style="width: 100px; border-radius: 10%;">
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    st.write("---")

        else:
            st.write("⚠️ Keine ähnlichen Spieler gefunden.")



#-----------------------------------------------------------------------------------------------------------------
        # Empfehlung von Spielen
        # Spiele aus dem Cluster
        cluster_games = player_cluster.groupby(["appid", "name"])["playtime_forever"].mean()  
        cluster_games = cluster_games.sort_values(ascending=False)
        cluster_favorite_games = cluster_games.head(10)  # Top 10 Spiele
        
        # Spiele, die der Nutzer besitzt
        user_games = set(user_data["appid"].unique())  

        # Spiele aus dem Cluster (Top 10)
        cluster_favorite_appids = set(cluster_favorite_games.index.get_level_values("appid").tolist())

        # Empfehlung: Nur Spiele aus dem Cluster, die der Spieler NICHT besitzt
        recommended_games = cluster_favorite_appids - user_games

        # Ausgabe der empfohlenen Spiele
        recommended_games_df = cluster_favorite_games.loc[cluster_favorite_games.index.get_level_values("appid").isin(recommended_games)]
        recommended_games_df = recommended_games_df.reset_index()[["appid", "name"]]

        # AppID als String umformatieren, um die Tausendertrennzeichen zu entfernen
        recommended_games_df["appid"] = recommended_games_df["appid"].astype(str)

        st.subheader("Diese Spiele könnten, dich interessieren:")
        st.write(recommended_games_df)


# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
    #76561198990374557 - paul.u1111
    #76561198254607847 - ImRizzex
    #76561198080617859 - ConCHEATER Wurst (Leopold Stotch)
    #76561197979048211 - floblak3
    #76561198364896644 - Yoink (Nathan)
    #76561198059410849 - jdvmb (viki)
    #76561198286398265 - theo_o (Daniel)
    #76561198128740874 - lennyte
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
