import streamlit as st
import requests

# URL de votre API FastAPI
api_url = "http://localhost:8000/recommandation"

# Interface utilisateur pour les entrées de l'utilisateur
st.title("Recommandation de Parfums")

# Entrée pour les parfums
parfums = st.text_input("Entrez les noms des parfums (séparés par une virgule):")

if st.button("Obtenir des recommandations"):
    # Faire une requête POST à l'API FastAPI avec les parfums en entrée
    response = requests.post(api_url, json={"parfum": parfums.split(",")})
    
    if response.status_code == 200:
        # Afficher les recommandations
        recommandations = response.json()
        st.write("Recommandations:")
        for nom, similarite in recommandations.items():
            st.write(f"{nom}: {similarite:.2f}")
    else:
        st.error("Erreur lors de la récupération des recommandations")

