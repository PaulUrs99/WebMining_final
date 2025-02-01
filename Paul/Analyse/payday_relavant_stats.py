# Manuelle Zuordnung von Beschreibungen zu den Statistiken
stat_descriptions = {
    "heist_success": "Erfolgreiche Überfälle",
    "heist_failed": "Gescheiterte Überfälle",
    "money_earned": "Gesamtverdienst",
    "money_spent": "Ausgegebenes Geld",
    "heist_stealth": "Stealth-Überfälle abgeschlossen",
    "heist_loud": "Laut abgeschlossene Überfälle",
    "total_kills": "Gesamte Kills",
    "total_headshots": "Kopfschüsse",
    "total_special_kills": "Spezialgegner getötet",
    "downs": "Anzahl der Niederlagen (zu Boden gehen)",
    "revives": "Anzahl der Wiederbelebungen",
    "accuracy": "Trefferquote (%)",
    "bullets_fired": "Abgefeuerte Kugeln",
    "bullets_hit": "Getroffene Kugeln",
    "hostages_taken": "Geiseln genommen",
    "money_bags_collected": "Gesicherte Geldsäcke",
    "loot_secured": "Gesicherte Beute insgesamt",
    "heist_most_played": "Meistgespielter Überfall",
    "play_time_hours": "Gesamtspielzeit (Stunden)",
    "deployables_used": "Verwendete Ausrüstungsgegenstände",
    "melee_kills": "Nahkampf-Kills",
    "sniper_kills": "Scharfschützen-Kills",
    "shotgun_kills": "Schrotflinten-Kills",
    "pistol_kills": "Pistolen-Kills",
    "assault_rifle_kills": "Sturmgewehr-Kills",
    "sentry_gun_kills": "Kills durch Sentry-Guns",
    "cameras_disabled": "Ausgeschaltete Kameras",
    "bags_carried": "Getragene Beutetaschen",
    "drills_placed": "Platzierte Bohrer",
    "drills_fixed": "Reparierte Bohrer",
    "civilians_killed": "Getötete Zivilisten",
    "stealth_attempts": "Versuchte Stealth-Überfälle",
    "contracts_completed": "Abgeschlossene Aufträge",
    "infamy_rank": "Infamy-Level (Prestige)",
    "highest_difficulty_completed": "Höchster abgeschlossener Schwierigkeitsgrad",
    "perk_decks_maxed": "Maximale Perk-Decks",
    "skills_maxed": "Maximale Skill-Level",
    "coop_games_played": "Gespielte Koop-Matches",
    "singleplayer_games_played": "Gespielte Einzelspieler-Matches",
    "player_level": "Spielerlevel",
}

# Automatisch Beschreibungen für die Waffenstatistiken generieren
for stat in final_filtered_df["Statistik"]:
    if "weapon_used" in stat:
        stat_descriptions[stat] = f"Waffe verwendet ({stat.split('_')[-1]})"
    elif "weapon_hits" in stat:
        stat_descriptions[stat] = f"Treffer mit Waffe ({stat.split('_')[-1]})"
    elif "weapon_kills" in stat:
        stat_descriptions[stat] = f"Kills mit Waffe ({stat.split('_')[-1]})"

# Eine DataFrame mit den Beschreibungen erstellen
final_filtered_df["Beschreibung"] = final_filtered_df["Statistik"].map(stat_descriptions)

# Die aktualisierte Liste anzeigen
tools.display_dataframe_to_user(name="Payday 2 Statistiken mit Beschreibungen", dataframe=final_filtered_df)
