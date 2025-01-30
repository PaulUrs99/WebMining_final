import streamlit as st

def app():

    st.title("Einloggen/Registrieren")

    auswahl = st.selectbox("Wähle eine Option", ["Einloggen", "Registrieren"])
    if auswahl == "Registrieren":

        # Registrieren
        st.title("Einloggen")
        benutzername = st.text_input("Benutzername")
        steam_id = st.number_input("Steam ID")
        epic_id = st.text_input("Epic ID")
        passwort = st.text_input("Passwort", type="password")
        if st.button("Einloggen"):
            st.write("Registrieren")
    
    else: 
        #Einloggen
        st.title("Einloggen")
        benutzername = st.text_input("Benutzername")
        passwort = st.text_input("Passwort", type="password")
        if st.button("Einloggen"):
            st.write("Einloggen erfolgreich")
