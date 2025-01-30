import streamlit as st
import pandas as pd
import Dashboard.APP as dashboard

def creds_entered():
    if st.session_state["user"].strip() == "admin" and st.session_state["pw"].strip() == "admin":
        st.session_state["authenticated"] = True
    else: 
        st.session_state["authenticated"] = False
        if not st.session_state["pw"]:
            st.warning("Bitte Passwort eingeben")
        elif not st.session_state["user"]:
            st.warning("Bitte Nutzernamen eingeben")
        else:
            st.error("Falsche Anmeldedaten")

def authenticate_user():
    if "authenticated" not in st.session_state:
        st.text_input(label="Username", key="user")
        st.text_input(label="Passwort", key="pw", type="password", on_change=creds_entered)
        return False
    else:
        if st.session_state["authenticated"]:
            return True
        else:
            st.text_input(label="Username", key="user")
            st.text_input(label="Passwort", key="pw", type="password", on_change=creds_entered)

if authenticate_user():
    # Hier wird das Dashboard bei erfolgreicher Authentifizierung geladen
    st.title("Hallo User")
    st.markdown("Willkommen zurück")
else:
    st.title("Platzhalter")
    st.markdown("Platzhalter")


