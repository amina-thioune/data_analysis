import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


st.title("Visualisation des données")
if 'data_name' in st.session_state:
    df = st.session_state['data_name']  # Accède directement au DataFrame stocké
    # Visualisation des variables catégorielles
    st.write("Visualisation des variables catégorielles")
    if df.select_dtypes(include=['object', 'category']).columns.empty:
        st.write("Aucune variable catégorielle trouvée.")
    else:
        variable = st.selectbox("Choisir une variable catégorielle", df.select_dtypes(include=['object', 'category']).columns)
        sns.set_style("darkgrid")
        fig, ax = plt.subplots(figsize=(20, 6))
        size_of_items = 20
        if len(df[variable].unique()) > 50:
            unique_categories = df[variable].unique()
            window = 50
            part = st.slider("Choisir la partie à afficher", 0, len(unique_categories) // window - 1)
            categories = unique_categories[part * window:part * window + window]
            sns.histplot(data=df[df[variable].isin(categories)][variable], ax=ax)
        else:
            sns.histplot(data=df[variable], ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        plt.xlabel('Catégorie')
        plt.ylabel('Fréquence')
        plt.title(f'Diagramme en barres: {variable}')
        st.pyplot(fig)
        ab=pd.DataFrame(df[variable].value_counts().sort_values(ascending=False)).head(size_of_items)
        st.write(ab)
else:
    st.write("Aucune donnée chargée. Veuillez retourner à l'accueil et télécharger un fichier.")