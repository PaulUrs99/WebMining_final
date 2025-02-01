import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def create_density_plot(data, player_value, title="Dichtefunktion", xlabel="Wert"):
    """
    Erstellt eine Dichtefunktion (KDE-Plot) mit einem hervorgehobenen Spielerwert.

    :param data: Liste oder Array mit numerischen Werten
    :param player_value: Der individuelle Spielerwert, der hervorgehoben wird
    :param title: Titel der Grafik
    :param xlabel: Beschriftung der x-Achse
    :return: Matplotlib-Figur für Streamlit
    """
    
    # Dunkles Theme setzen
    plt.style.use("dark_background")

    # Größe und Format
    fig, ax = plt.subplots(figsize=(4, 2), dpi=100)
    fig.patch.set_facecolor("#0E1117")  # Hintergrund schwarz
    ax.set_facecolor("#0E1117")  # Diagrammhintergrund schwarz
    
    # Dichtefunktion zeichnen
    sns.kdeplot(data, ax=ax, color="#3498db", linewidth=1.5)
    
    # Spielerwert als vertikale Linie einzeichnen
    ax.axvline(player_value, color="red", linestyle="dashed", linewidth=1, label="Spielerwert")
    ax.set_xlabel(xlabel, color="white", fontsize=6)
    ax.set_ylabel("Dichte (%)", color="white", fontsize=6)
    ax.set_title(title, color="white", fontsize=7)
    ax.tick_params(axis="both", colors="white", labelsize=6)
    ax.legend(facecolor="#0E1117", edgecolor="white", fontsize=5, loc="upper right")
    
    return fig 
