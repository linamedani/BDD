from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json

# Charger les variables d'environnement
load_dotenv(".env")
uri = os.getenv("MONGODB_URI")

# Créer un nouveau client et se connecter au serveur
client = MongoClient(uri, server_api=ServerApi('1'))

# Envoyer un ping pour confirmer une connexion réussie
try:
    client.admin.command('ping')
    print("Connexion réussie à MongoDB !")
except Exception as e:
    print(f"Erreur de connexion : {e}")

# Accéder à la base de données
db = client.bd

def get_arrival_ville(departure_ville):
    try:
        villes = db.vols.distinct("VilleA", {"VilleD": departure_ville})
        if villes:
            return villes
        else:
            return f"Aucune ville d'arrivée trouvée pour la ville de départ : {departure_ville}"
    except Exception as e:
        return f"Une erreur s'est produite : {e}"

def compter_pilotes_par_lettre_mongo(lettre):
    try:
        # Utiliser l'agrégation pour extraire les noms des pilotes
        pipeline = [
            {
                "$unwind": "$Pilote"  # Déplier les documents liés au pilote
            },
            {
                "$match": {
                    "Pilote.NomPil": {"$regex": lettre, "$options": "i"} 
                      # Rechercher par lettre dans le nom du pilote
                }
            },
            {
                "$group": {
                    "_id": "$Pilote.NomPil"  # Regrouper par nom de pilote
                }
            }
        ]
        
        # Exécuter le pipeline d'agrégation
        resultats = db.vols.aggregate(pipeline)
        # Compter le nombre de pilotes uniques
        count = sum(1 for _ in resultats)
        return count
    except Exception as e:
        return f"Une erreur s'est produite : {e}"

# Exemple d'utilisation
lettre_recherchee = "a"  # Remplacez par la lettre que vous souhaitez rechercher
nombre_de_pilotes = compter_pilotes_par_lettre_mongo(lettre_recherchee)
print(f"Nombre de pilotes contenant la lettre '{lettre_recherchee}': {nombre_de_pilotes}")

# Exemple d'utilisation
if __name__ == "__main__":
    print(get_arrival_ville("Marseille"))
  

