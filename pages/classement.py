import streamlit as st

# Sélectionner un modèle
modele = st.selectbox(
    'Moséle à  utiliser',
    ('Arbre de décision', 'Random forest'),
    index=None,
    placeholder="sélectionnez un modéle",)