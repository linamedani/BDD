from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from os import getenv

load_dotenv(".env")
uri = getenv("MONGODB_URI")

# Créez un nouveau client et connectez-vous au serveur
client = MongoClient(uri, server_api=ServerApi('1'))

# Envoyez un ping pour confirmer une connexion réussie
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Accéder à une base de données
db = client.test  # Remplacez 'test' par le nom de votre base de données

# Insérer un document
result = db.utilisateurs.insert_one({"nom": "Alice", "age": 30, "ville": "Paris"})
print("Document inséré avec l'ID :", result.inserted_id)

# Vérifier les données insérées
utilisateurs = db.utilisateurs.find()
for utilisateur in utilisateurs:
    print(utilisateur)

