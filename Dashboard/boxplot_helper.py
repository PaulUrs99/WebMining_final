import matplotlib.pyplot as plt

def create_boxplot(percentiles, player_value, title="Boxplot", xlabel="Wert"):
    """
    Erstellt einen sehr kompakten horizontalen Boxplot mit kleinem Text und kleiner Legende.
    
    :param percentiles: Dictionary mit Perzentilwerten (z. B. {"1%": 0.5, "50%": 1.5, "99%": 4.0})
    :param player_value: Der individuelle Spielerwert, der hervorgehoben wird
    :param title: Titel der Grafik
    :param xlabel: Beschriftung der x-Achse
    :return: Matplotlib-Figur für Streamlit
    """

    # Dunkles Theme setzen
    plt.style.use("dark_background")

    # Erstelle das Diagramm in kompakter Größe
    fig, ax = plt.subplots(figsize=(4, 1.5), dpi=100)  # Sehr kleine Grafik
    fig.patch.set_facecolor("#0E1117")  # Hintergrund schwarz
    ax.set_facecolor("#0E1117")  # Diagrammhintergrund schwarz

    # Boxplot-Stil anpassen
    boxprops = dict(facecolor="#3498db", color="white", linewidth=0.8)  # Dünnere Linien
    medianprops = dict(color="#e74c3c", linewidth=1)  # Dünnere Median-Linie
    whiskerprops = dict(color="white", linewidth=0.8)  # Dünnere Whiskers
    capprops = dict(color="white", linewidth=0.8)  # Dünnere Enden
    flierprops = dict(marker="o", color="white", markersize=1)  # Kleinere Ausreißerpunkte

    # Erstelle den horizontalen Boxplot
    ax.boxplot(list(percentiles.values()), vert=False, patch_artist=True,
               boxprops=boxprops, medianprops=medianprops,
               whiskerprops=whiskerprops, capprops=capprops, flierprops=flierprops)

    # Spielerwert als roten Punkt hinzufügen
    ax.axvline(player_value, color="red", linestyle="dashed", linewidth=0.5, label="Spielerwert") 

    # Achsen & Titel formatieren
    ax.set_yticks([1])
    ax.set_yticklabels([""], color="white", fontsize=6)  # Kleiner Text
    ax.set_xlabel(xlabel, color="white", fontsize=6)
    ax.set_title(title, color="white", fontsize=7)

    # Tick-Labels anpassen
    ax.tick_params(axis="x", colors="white", labelsize=6)

    # Kleine Legende anzeigen
    ax.legend(facecolor="#0E1117", edgecolor="white", fontsize=4, loc="upper right")

    return fig  # Gibt das Matplotlib-Objekt zurück
