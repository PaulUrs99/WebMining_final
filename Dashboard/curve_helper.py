import matplotlib.pyplot as plt

def create_percentile_curve(percentiles, player_value, title="Perzentilkurve", xlabel="Wert"):
    """
    Erstellt eine kompakte Perzentilkurve mit kleinem Text und einer Markierung für den Spielerwert.
    
    :param percentiles: Dictionary mit Perzentilwerten (z. B. {"1%": 0.5, "50%": 1.5, "99%": 4.0})
    :param player_value: Der individuelle Spielerwert, der hervorgehoben wird
    :param title: Titel der Grafik
    :param xlabel: Beschriftung der x-Achse
    :return: Matplotlib-Figur für Streamlit
    """
    
    # Dunkles Theme setzen
    plt.style.use("dark_background")
    
    # Erstelle das Diagramm in kompakter Größe
    fig, ax = plt.subplots(figsize=(4, 2), dpi=100)
    fig.patch.set_facecolor("#0E1117")  # Hintergrund schwarz
    ax.set_facecolor("#0E1117")  # Diagrammhintergrund schwarz
    
    # Perzentile als Linie zeichnen
    percentile_keys = [int(p.strip('%')) for p in percentiles.keys()]
    percentile_values = list(percentiles.values())
    ax.plot(percentile_keys, percentile_values, marker="o", color="#3498db", linewidth=1, markersize=2, label="Perzentilwerte")
    
    # Spielerwert als vertikale rote Linie hinzufügen
    ax.axhline(player_value, color="red", linestyle="dashed", linewidth=0.5, label="Spielerwert")
    
    # Achsen & Titel formatieren
    ax.set_xticks([0, 25, 50, 75, 100])  # Wichtige Perzentile markieren
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], color="white", fontsize=6)
    ax.set_xlabel("Perzentile", color="white", fontsize=6)
    ax.set_ylabel(xlabel, color="white", fontsize=6)
    ax.set_title(title, color="white", fontsize=7)
    
    # Tick-Labels anpassen
    ax.tick_params(axis="y", colors="white", labelsize=6)
    ax.tick_params(axis="x", colors="white", labelsize=6)
    
    # Kleine Legende anzeigen
    ax.legend(facecolor="#0E1117", edgecolor="white", fontsize=5, loc="upper left")
    
    return fig  # Gibt das Matplotlib-Objekt zurück
