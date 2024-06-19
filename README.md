# Projet de Site Web avec Streamlit

Ce projet consiste en un site web interactif développé avec Streamlit, une plateforme open-source permettant de créer facilement des applications web pour le traitement et l'analyse de données.

## Description

L'application développée dans ce projet vise à fournir une interface conviviale pour l'exploration, la visualisation et le classement des données. Elle permet aux utilisateurs, par binôme, d'analyser les données afin de classer les candidats pour divers départements académiques, y compris le département informatique.

## Fonctionnalités

- **Accueil :** permet de charger tout type de fichier pour l'analyse.
  
- **Exploration des Données :** onglet dédié à l'exploration approfondie des données de Parcoursup.

- **Visualisation :** Utilisation de bibliothèques de data science comme Pandas, Matplotlib et Seaborn pour visualiser les données de manière informative.

- **Réduction de Dimension :** Techniques telles que PCA, FAMD et SVD pour simplifier la visualisation et l'analyse des données.

- **Classement :** Implémentation d'algorithmes de machine learning pour évaluer et classer les candidats selon divers critères.

- **Aide (Chatbot) :** Intégration d'un chatbot utilisant un LLM Mistral pour répondre à toutes les questions relatives aux notions utilisées dans l'application.

## Technologies Utilisées

- **Streamlit :** Framework Python pour la création d'applications web interactives.

- **Python :** Langage de programmation principal pour le développement.

- **Pandas, Matplotlib, Seaborn :** Bibliothèques de data science utilisées pour l'analyse et la visualisation des données.

- **Firebase :** Utilisé pour le stockage sécurisé des données et l'interaction avec la base de données.

## Comment Exécuter Localement

1. Clonez ce dépôt sur votre machine locale.
   
   ```bash
   git clone https://github.com/votre_utilisateur/sae.git
   ```
   
2. Installez les dépendances nécessaires.

   ```bash
   pip install -r requirements.txt
   ```
   
3. Lancez l'application Streamlit.

   ```bash
   streamlit run main.py
   ```

4. Ouvrez votre navigateur et accédez à l'URL locale fournie par Streamlit pour explorer l'application.
