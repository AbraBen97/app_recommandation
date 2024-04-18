from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Créez une instance FastAPI
app = FastAPI()
np.random.seed(0)

# Définition de la classe d'entrée de prédiction
class EntreePrediction(BaseModel):
    parfum: List[str]  # Liste de chaînes de caractères (noms des parfums)

# Chargement des données
df_concat = pd.read_csv("donnees_propres.csv")
df_concat.set_index('nom', inplace=True)

# Fonction de prédiction
def prediction(*parfums):
    global df_concat
    new_user = np.zeros(df_concat.shape[1])  # Initialisation d'une série de zéros

    # Calcul du nouveau profil utilisateur
    for parfum in parfums:
        new_user += df_concat.loc[parfum]
    new_user[new_user > 1] = 1  # Limite à 1
    df_concat.loc['new_user'] = new_user
    
    # Calcul de la similarité de Jaccard
    jaccard_distances = pdist(df_concat.values, metric='jaccard')
    jaccard_similarity_array = 1 - squareform(jaccard_distances)
    jaccard_similarity_df = pd.DataFrame(jaccard_similarity_array, index=df_concat.index, columns=df_concat.index)
    
    # Récupération des similarités pour le nouvel utilisateur
    jaccard_similarity_series = jaccard_similarity_df.loc['new_user']
    
    # Suppression des parfums d'entrée
    jaccard_similarity_series = jaccard_similarity_series.drop(list(parfums))
    
    # Trier les valeurs de similarité de la plus élevée à la plus basse
    ordered_similarities = jaccard_similarity_series.sort_values(ascending=False)
    
    # Supprimer le profil utilisateur après la prédiction
    df_concat = df_concat.drop(index='new_user')
    
    L = ordered_similarities[1:6]
    dic = { L.index[0]: L.values[0],L.index[1]: L.values[1],L.index[2]: L.values[2],L.index[3]: L.values[3],
           L.index[4]: L.values[4]}
        
    return dic

@app.get("/")
def acceuil():
    return {"message": "Bienvenue sur notre API de recommandation de parfums"}

@app.post("/recommandation")
def predire(donne: EntreePrediction):
    recommandations = prediction(*donne.parfum)
    
    return recommandations
