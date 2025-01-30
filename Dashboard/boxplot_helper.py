import matplotlib.pyplot as plt

def create_boxplot(percentiles, player_value, title="Boxplot", ylabel="Wert"):
    """
    Erstellt einen Boxplot mit einem markierten Spielerwert.
    
    :param percentiles: Dictionary mit Perzentilwerten (z. B. {"1%": 0.5, "50%": 1.5, "99%": 4.0})
    :param player_value: Der individuelle Spielerwert, der hervorgehoben wird
    :param title: Titel der Grafik
    :param ylabel: Beschriftung der y-Achse
    :return: Matplotlib-Figur für Streamlit
    """

    # Setze den dunklen Hintergrund
    plt.style.use("dark_background")

    # Erstelle das Diagramm
    fig, ax = plt.subplots(figsize=(4, 5), dpi=100)
    fig.patch.set_facecolor("#0E1117")  # Hintergrund schwarz
    ax.set_facecolor("#0E1117")  # Diagrammhintergrund schwarz

    # Boxplot-Stil anpassen
    boxprops = dict(facecolor="#3498db", color="white")  # Blaue Box, weiße Umrandung
    medianprops = dict(color="#e74c3c", linewidth=2)  # Rote Median-Linie
    whiskerprops = dict(color="white")  # Weiße Whiskers
    capprops = dict(color="white")  # Weiße Enden der Whiskers
    flierprops = dict(marker="o", color="white", markersize=5)  # Weiße Punkte für Ausreißer

    # Erstelle den Boxplot basierend auf den Perzentilen
    ax.boxplot(list(percentiles.values()), vert=True, patch_artist=True,
               boxprops=boxprops, medianprops=medianprops,
               whiskerprops=whiskerprops, capprops=capprops, flierprops=flierprops)

    # Spielerwert als roten Punkt hinzufügen
    ax.scatter(1, player_value, color='red', zorder=3, label="Spielerwert", s=60)

    # Achsen & Titel formatieren
    ax.set_xticks([1])
    ax.set_xticklabels([ylabel], color="white")
    ax.set_ylabel(ylabel, color="white")
    ax.set_title(title, color="white")

    # Tick-Labels anpassen
    ax.tick_params(axis="y", colors="white")

    # Legende anzeigen
    ax.legend(facecolor="#0E1117", edgecolor="white")

    return fig  # Gibt das Matplotlib-Objekt zurück
