import streamlit as st
import pandas as pd
import numpy as np

# Titel und Beschreibung
st.title("Beispiel-Dashboard")
st.markdown("Dieses Dashboard zeigt interaktive Beispiele mit Streamlit.")

# Eingabefelder
name = st.text_input("Wie heißt du?")
st.write(f"Hallo, {name}!")

# Slider für numerischen Wert
number = st.slider("Wähle eine Zahl:", 0, 100, 50)
st.write(f"Deine ausgewählte Zahl ist {number}.")

# Beispiel-Daten generieren
data = pd.DataFrame(
    np.random.randn(100, 2) * 50,
    columns=["X-Werte", "Y-Werte"]
)

# Diagramm anzeigen
st.subheader("Streudiagramm der generierten Daten:")
st.scatter_chart(data)

# Checkbox
if st.checkbox("Zeige Daten an"):
    st.dataframe(data)
