import streamlit as st
import pandas as pd
from fonctions.nettoyage import *

# Fonction pour calculer la corrélation entre les variables numériques
def calculate_correlation(df, numerical_variables, variable):
    threshold=0.6
    correlated_dict = {}
    correlations = df[numerical_variables].corrwith(df[variable])
    correlated_vars =[(df[numerical_variables].columns[j], corr) for j, corr in enumerate(correlations) if abs(corr) >= threshold]
    if correlated_vars:
        correlated_dict[variable] = correlated_vars
    return correlated_dict

# Header de la page
st.title("🔍  Exploration de données")

# Récupération du dataframe depuis la session
if "data_name" in st.session_state:
    df = st.session_state["data_name"]

    # Afficher le DataFrame avec différentes options
    st.subheader("Afficher le dataframe")
    option_df = st.selectbox(
        "Veuillez choisir les variables que vous voulez afficher",
        ("Tout", "Variables Numériques", "Variables Catégorielles"))

    if option_df == "Tout":
        st.dataframe(df)
    elif option_df == "Variables Numériques":
        st.dataframe(df.select_dtypes(include=['int64', 'float64']))
    elif option_df == "Variables Catégorielles":
        st.dataframe(df.select_dtypes(include=['object', 'category']))

    # Afficher la description des données
    st.subheader("Description des données")
    option_desc = st.selectbox(
        "Choisissez le type de variables pour afficher leurs statistiques descriptives",
        ("Variables Numériques", "Variables Catégorielles"))

    if option_desc == "Variables Numériques":
        st.dataframe(df.select_dtypes(include=['int64', 'float64']).describe())
    elif option_desc == "Variables Catégorielles":
        st.dataframe(df.select_dtypes(include=['object', 'category']).describe())

    # Filtrer les valeurs NaN
    st.subheader("Filtrage des valeurs NaN")
    percentage_nan = st.slider("Choisissez le pourcentage de NaN à filtrer", 0, 100, 0)
    threshold =  df.isnull().mean() * 100
    columns_to_display = threshold[threshold >= percentage_nan].index
    st.dataframe(df[columns_to_display])
    st.write("Colonnes de type 'object' ou 'category' avec pourcentage de valeurs manquantes:")
    st.dataframe(columns_to_display)


    # Afficher la corrélation entre les variables numériques
    st.subheader("Corrélation entre les variables numériques")
    df,numerical_variables, categorical_variables = nettoyage(df)
    variable_corr = st.selectbox("Choisissez une variable numérique", numerical_variables)
    correlations = calculate_correlation(df, numerical_variables, variable_corr)
    if correlations:
        st.write(f'Variables corrélées avec {variable_corr} :')
         # Créer un DataFrame pour les résultats de corrélation
        correlation_data = {
                'Variables': [var for var, _ in correlations[variable_corr]],
                'Corrélation': [corr for _, corr in correlations[variable_corr]]
            }
        correlation_df = pd.DataFrame(correlation_data)

            # Afficher le DataFrame
        st.dataframe(correlation_df)
    else:
        st.write(f'Aucune variable avec {variable_corr}')


else:
    st.warning("Veuillez charger un fichier svp !",  icon="⚠️")