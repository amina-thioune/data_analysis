import streamlit as st
import pandas as pd

st.title("Exploration des données")
#Récuperer le dataframe 
if "data_name" in st.session_state :
    df = st.session_state["data_name"]
else : 
    st.warning('Veuillez charger un fichier svp !', icon="⚠️")


# Afficher le dataframe
option = st.selectbox(
    "Veuillez choisir les variables que vous voulez afficher",
    ("Tout", "Variables numériques", "Variables Catégorielles"))

if option == "Tout" : 
    st.dataframe(df)

elif option =="Variables Catégorielles" :
     # Sélectionner les colonnes numériques et catégorielles
    numeric_and_categorical_variables = []
    for column in df.columns:
        # Vérifier si la colonne contient au moins une valeur numérique
        if any(isinstance(val, (int, float)) for val in df[column] if not pd.isna(val)):
            numeric_and_categorical_variables.append(column)
    categorical_variables = df.select_dtypes(include="O").columns.tolist()
    # Sélectionner uniquement les variables qui n'ont aucune valeur numérique
    categorical_variables = list(set(categorical_variables).difference(numeric_and_categorical_variables))

    st.dataframe(df[categorical_variables])

elif option == "Variables numériques" : 
     # Sélectionner les colonnes numériques et catégorielles
    numeric_and_categorical_variables = []
    for column in df.columns:
        # Vérifier si la colonne contient au moins une valeur numérique
        if any(isinstance(val, (int, float)) for val in df[column] if not pd.isna(val)):
            numeric_and_categorical_variables.append(column)
    
    numerical_variables = numeric_and_categorical_variables
    st.dataframe(df[numerical_variables])