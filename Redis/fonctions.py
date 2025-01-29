import redis
import json

# Initialisation de Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Vérifiez que la connexion fonctionne
try:
    r.ping()
    print("Connecté à Redis")
except redis.ConnectionError:
    print("Erreur de connexion à Redis")


# Fonction pour lister les villes d'arrivée
def lister_villes_arrivee(r, ville_depart):
    villes_arrivee = set()
    keys = r.keys("vol:*")  # Récupérer toutes les clés de vols
    for key in keys:
        vol_data = json.loads(r.get(key))  # Récupérer les données de chaque vol
        if vol_data.get("VilleD") == ville_depart:  # Vérifier la ville de départ
            villes_arrivee.add(vol_data.get("VilleA"))  # Ajouter la ville d'arrivée
    return list(villes_arrivee)

# Fonction pour compter les pilotes par lettre
def compter_pilotes_par_lettre(r, lettre):
    pilotes_uniques = set()  # Ensemble pour stocker les pilotes uniques
    keys = r.keys("vol:*")  # Récupérer toutes les clés de vols
    for key in keys:
        vol_data = json.loads(r.get(key))  # Récupérer les données de chaque vol
        pilote = vol_data.get("Pilote", {})  # Récupérer les informations du pilote
        if pilote and lettre.lower() in pilote["NomPil"].lower():  # Vérifier la présence de la lettre
            pilotes_uniques.add(pilote["NomPil"])  # Ajouter le nom du pilote à l'ensemble
    return len(pilotes_uniques)  # Retourner le nombre de pilotes uniques

# Utilisation de la fonction lister_villes_arrivee
ville_depart = "Paris"  # Exemple de ville de départ
villes_arrivees = lister_villes_arrivee(r, ville_depart)  # Inclure r comme argument
print("Villes d'arrivée depuis", ville_depart, ":", villes_arrivees)

# Utilisation de la fonction compter_pilotes_par_lettre
lettre = "a"  # Exemple de lettre à chercher
nombre_pilotes = compter_pilotes_par_lettre(r, lettre)  # Passer r comme argument
print("Nombre de pilotes uniques contenant la lettre", lettre, ":", nombre_pilotes)
