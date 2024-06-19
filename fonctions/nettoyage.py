import pandas as pd
from sklearn.impute import SimpleImputer



def nettoyage(data) : 
    """
     Cette fonction effectue plusieurs opérations de nettoyage sur un jeu de données.

        Paramètre :
            data : le DataFrame contenant les données à nettoyer.

        Retour : 
            Le Dataframe nettoyé
            La liste des noms des variables numériques.
            La liste des noms des variables catégorielles.
    """
    # Supprimer les colonnes qui contient que des Nan
    data_NaN = data.loc[:, data.isna().sum() == data.shape[0]]
    data = data.drop(columns=data_NaN.columns.tolist())
    # Selectionner les colonnes datetime
    datetime_columns = data.select_dtypes(include=['datetime64']).columns
    # Supprimer
    data.drop(columns=datetime_columns, inplace=True)

    numeric_and_categorical_variables = []
    for column in data.columns:

    # Vérifier si la colonne contient au moins une valeur numérique
        if any(isinstance(val, (int, float)) for val in data[column] if not pd.isna(val)):
            numeric_and_categorical_variables.append(column)
    numerical_variables = numeric_and_categorical_variables
    categorical_variables = data.select_dtypes(include="O").columns.tolist()

    # Sélectionner uniquement les variables qui n'ont aucune valeur numérique
    categorical_variables = list(set(categorical_variables).difference(numeric_and_categorical_variables))
        
    # Remplacer les chaines de caractères dans les variables numériques par NaN
    for var in numerical_variables:
        data[var] = pd.to_numeric(data[var], errors='coerce')

    # Imputer avec la moyenne
    imputer_numerical = SimpleImputer(strategy='mean')
    data[numerical_variables] = imputer_numerical.fit_transform(data[numerical_variables])

    # Imputer avec les plus fréquents
    for col in categorical_variables:
        most_frequent_value = data[col].value_counts().idxmax()
        data[col].fillna(most_frequent_value, inplace=True)
    
    return data, numerical_variables, categorical_variables 
