import streamlit as st
import pandas as pd


st.title("Accueil du site")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) # utiliser --server.maxUploadSize 500 pour modifier la taille max du fichier
    st.session_state["data_name"] = df
    st.write(df)
else :
    st.warning("Veuillez choisir un jeu de données")