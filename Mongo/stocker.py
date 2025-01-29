import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from os import getenv
import time
# Charger les variables d'environnement depuis le fichier .env
load_dotenv(".env")
uri = getenv("MONGODB_URI")
client = MongoClient(uri, server_api=ServerApi('1'))# Créer un client MongoDB
try:# Envoyer un ping pour confirmer une connexion réussie
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client.bd  # Accéder à la base de données et à la collection
# Chemin du fichier JSON à lire
input_file = 'vols_final.json'# Lire le contenu du fichier JSON
with open(input_file, 'r') as f:
    vols_final = json.load(f)
start_time = time.time() # Mesurer le temps d'insertion
for vol in vols_final.values():# Insérer les vols dans MongoDB
    result = db.vols.insert_one(vol)  # la collection
    print(f"Document inséré avec l'ID : {result.inserted_id}")
print(f"Nombre de vols à insérer : {len(vols_final)}")
insertion_time = time.time() - start_time
print(f"Temps d'insertion dans MongoDB : {insertion_time:.4f} secondes")
start_time = time.time()# Mesurer le temps de lecture
for doc in db.vols.find(): 
    pass
reading_time = time.time() - start_time
print(f"Temps de lecture dans MongoDB : {reading_time:.4f} secondes")

