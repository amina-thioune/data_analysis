import os
import sys 
package_dir = os.getcwd() # C:\\Users\\amina\\SAE
sys.path.append(os.path.join(package_dir, "pages"))
import streamlit as st
from fonctions.nettoyage import *
from fonctions.encoder import *
from modeles.tree_decision import tree_decision
from sklearn import tree
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix
from pickle import dump
from pickle import load
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


# Configurer la page pour utiliser toute la largeur
st.set_page_config(layout="wide")
st.title("🥇 Classification")

#Récuperer le dataframe 
if "data_name" in st.session_state :
    df = st.session_state["data_name"]


    #Modèle linéaire
    st.sidebar.title("Modèle de classification")
    # Sélectionner un modèle
    modele_lineaire = st.sidebar.selectbox(
        'Choisissez un modèle',
        ('Tree Decision', 'Linear SVM', 'Random Forest'),
        index=None,
        placeholder="sélectionnez un modéle",)
    

    if modele_lineaire == 'Tree Decision':
        train = st.sidebar.radio("Inférence ou training", ['***Training***', '***Inférence***'])  

        if train == '***Training***' :
            # Choisir variable cible    
            cible  = st.sidebar.selectbox("Choisir la variable cible", df.columns.tolist())
            y = df[cible]
            X = df.drop(cible, axis=1)
                      
            # Variables à supprimer
            supprime_variables  = st.sidebar.multiselect("Choisir des variables à supprimer", X.columns.tolist())
            
            X, numerical_variables, categorical_variables = nettoyage(X)
            # Prétraitement des données
            pretraitement = st.sidebar.radio("Gestion des variables catégorielles :",
            ["***Supprimer***", "***Encoder***"],
            index=None)
            if pretraitement  == "***Supprimer***":
                X = X.drop(columns=categorical_variables, axis=1)
            if pretraitement  =="***Encoder***" :
                X = encoder(X,numerical_variables, categorical_variables)

            # choisir x_test et y_train
            pourcentage  = st.sidebar.slider("Pourcentage train", 5, 100, 80)
            size =int(X.shape[0] * (pourcentage/100))
            X_train = X.loc[:size, :]
            y_train = y.loc[:size]
            X_test = X.loc[size:, :]
            y_test = y.loc[size:]
            
           
        
            # Soumettre ses choix
            soumettre = st.sidebar.button("Run", type="primary", use_container_width=True)


            if soumettre:
                     # Supprimer les variables du dataframe
                    X_train = X_train.drop(supprime_variables, axis=1)
                    X_test_supprimer = X_test[supprime_variables]
                    X_test = X_test.drop(supprime_variables, axis=1)

                    # Entrainer le modèle
                    clf = tree_decision(X_train, y_train)

                    # Prédire sur les données  de test
                    y_pred = clf.predict(X_test)

                    # Calculer accuracy
                    accuracy = accuracy_score(y_test, y_pred)

                    # Calculer precision
                    precision = precision_score(y_test, y_pred, average='weighted')

                    # Calculer recall
                    recall = recall_score(y_test, y_pred, average='weighted')

                    # Calculer F1-score
                    f1 = f1_score(y_test, y_pred, average='weighted')

                    # Mettre les indicateurs de performance dans un dataframe
                    st.title("Indicateurs de performance")
                    st.dataframe({"mesures" : ["Accuracy", "Precision", "Recall", "F1_Score"], "valeur" :[accuracy, precision, recall, f1]}, column_config={"mesures": "Mesures", "valeur" : "Valeurs"})
                
                    # Matrice de confusion
                    conf_matrix = confusion_matrix(y_test, y_pred, labels=y.unique().tolist())


                    # Tracez la matrice de confusion en utilisant Seaborn
                    st.title("Matrice de Confusion")
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap="Blues", ax=ax)
                    ax.set_xlabel('Predicted labels')
                    ax.set_ylabel('True labels')
                    ax.set_title('Confusion Matrix')
                    st.pyplot(fig)

                    # Réinitialisation des index
                    X_test_supprimer = X_test_supprimer.reset_index(drop=True)
                    X_test = X_test.reset_index(drop=True)

                    # Predict sur X
                    predict = clf.predict(X_test)
                    st.title("Prédiction sur le dataframe")
                    df_predict = pd.DataFrame(predict, columns=['Prediction'])
                    df_predict = df_predict.reset_index(drop=True)                
                    st.dataframe(pd.concat([X_test, df_predict], axis= 1))
                   
                    # Predict prob sur X
                    predict_proba = clf.predict_proba(X_test)
                    st.title("Probabilité pour qu'un inddividu appartient à une classe")
                    df_predict_proba = pd.DataFrame(predict_proba.max(axis=1), columns=['Probability'])
                    df_predict_proba = df_predict_proba.reset_index(drop=True)
                    st.dataframe(pd.concat([X_test, pd.DataFrame(predict_proba)], axis= 1))                                         

                    # Creer un nouveau dataframe à partir de df en rajoutant deux colonnes la classe(résultat de predict) et les probas avec (predict prob)                    
                    df_classer = pd.concat([X_test_supprimer, X_test, df_predict, df_predict_proba], axis=1)
                    
                    # Afficher nouveau df
                    st.title("Jeu de données avec les classements")
                    st.dataframe(df_classer)

                    # Sauvegarder modèle
                    with open("tree_decision.pkl", "wb") as file :
                        dump(clf, file, protocol=5)


        # Inference
        elif train == '***Inférence***':

            # 3 Charger un model
            with open("tree_decision.pkl", "rb") as file:
                clf = load(file)

            # Vérifier si les colonnes sont égaux
            if df.shape[1] == clf.n_features_in_ : 
                    
                # 4. predire
                predict = clf.predict(df)

                # Afficher résultat   
                df_predict = pd.DataFrame(predict, columns=['Prediction'])
                df_classer = pd.concat([df, df_predict], axis=1)
                st.title("Jeu de données avec les prédictions")
                st.dataframe(df_classer)

            else : 
                st.warning("Les colonnes de votre jeu de données doivent être égales à " + str(clf.n_features_in_), icon="⚠️")


else :
    st.warning("Veuillez charger un fichier svp !",  icon="⚠️")