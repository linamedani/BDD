import os
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv(".env")
uri = os.getenv("MONGODB_URI")

# Créer un client MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['bd']  # La base de données

# Dictionnaire de correspondance
table_correspondance = {
    "AVIONS.txt": ["NumAv", "NomAv", "CapAv", "VilleAv"],
    "CLIENTS.txt": ["NumCl", "NomCl", "NumRueCl", "NomRueCl", "CodePosteCl", "VilleCl"],
    "DEFCLASSES.txt": ["NumVol", "Classe", "CoefPrix"],
    "PILOTES.txt": ["NumPil", "NomPil", "NaisPil", "VillePil"],
    "RESERVATIONS.txt": ["NumCl", "NumVol", "Classe", "NbPlaces"],
    "VOLS.txt": ["NumVol", "VilleD", "VilleA", "DateD", "HDtime", "DateA", "HAtime", "NumPil", "NumAv"],
}


# Dictionnaire principal pour stocker les données
dict_data = {key: [] for key in table_correspondance.keys()}

# Charger les fichiers .txt dans dict_data
for filename, columns in table_correspondance.items():
    with open(filename, 'r') as file:
        for line in file:
            data = line.strip().split('\t')  # Séparer les données par des tabulations
            record = {columns[i]: data[i] for i in range(len(columns))}
            dict_data[filename].append(record)

print("Données chargées :", dict_data)

# Dictionnaire pour le JSON final
vols_final = {}

for vol in dict_data["VOLS.txt"]:
    num_vol = vol["NumVol"]
    vols_final[num_vol] = {
        "NumVol": num_vol,
        "VilleD": vol["VilleD"],
        "VilleA": vol["VilleA"],
        "DateD": vol["DateD"],
        "HD Time": vol["HDtime"],
        "DateA": vol["DateA"],
        "HAtime": vol["HAtime"],
        "Avion": next((av for av in dict_data["AVIONS.txt"] if av["NumAv"] == vol.get("NumAv")), {}),
        "Pilote": next((pil for pil in dict_data["PILOTES.txt"] if pil["NumPil"] == vol.get("NumPil")), {}),
        "Clients": []  # Liste pour stocker les clients associés
    }

    # Trouver toutes les réservations pour le vol actuel
    reservations = [res for res in dict_data["RESERVATIONS.txt"] if res["NumVol"] == num_vol]

    for reservation in reservations:
        client_info = next((client for client in dict_data["CLIENTS.txt"] if client["NumCl"] == reservation["NumCl"]), {})
        vols_final[num_vol]["Clients"].append({
            "NumClient": reservation["NumCl"],
            "NomClient": client_info.get("NomCl", ""),
            "NombrePlaces": reservation["NbPlaces"],
            "Classe": reservation["Classe"]
        })

# Afficher le JSON final pour vérifier
print("JSON final dénormalisé :", json.dumps(vols_final, indent=4))

# Sauvegarder le JSON final dans un fichier
with open('vols_final.json', 'w') as json_file:
    json.dump(vols_final, json_file, indent=4)

print("Le JSON final a été sauvegardé dans 'vols_final.json'.")