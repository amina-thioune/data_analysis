from sklearn.preprocessing import LabelEncoder


def encoder(df,numerical_variables, categorical_variables) :

    """
        Cette fonction nettoie et prépare un jeu de données en supprimant les colonnes à faible valeur informative 
        et en encodant les variables catégorielles.

        Paramètres :
            - df : le jeu de données initial.
            - numerical_variables  : liste des noms des colonnes numériques.
            - categorical_variables  : liste des noms des colonnes catégorielles.

        Retour :
            - data : le jeu de données nettoyé et préparé avec les variables catégorielles encodées.
    """
            
    # Supprimer les colonnes numériques avec une très faible variance
    threshold = .8 * (1 - .8)
    numeric_cols_low_variance = df[numerical_variables].columns[df[numerical_variables].var() < threshold]
    df.drop(columns=numeric_cols_low_variance, inplace=True)

    # Supprimer les colonnes catégorielles avec une seule catégorie
    categorical_cols_one_category = df[categorical_variables].columns[df[categorical_variables].nunique() == 1]
    df.drop(columns=categorical_cols_one_category, inplace=True)

    # Mise à jour des variables
    numerical_variables = list(set(numerical_variables).difference(numeric_cols_low_variance))
    categorical_variables = list(set(categorical_variables).difference(categorical_cols_one_category))

    #Initialiser LabelEncoder
    data = df.copy()

    label_encoder = LabelEncoder()

    # Parcourir chaque variable catégorielle et l'encoder
    for col in categorical_variables:
        data[col] = label_encoder.fit_transform(data[col])

    return data