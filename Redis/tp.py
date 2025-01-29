import json
import os
import redis


# création d'une table de correspondance (on créé un nom aux colonnes)
tableCorespondance={"AVIONS.txt":["NumAv","NomAv","CapAv","VilleAv"],
                    "CLIENTS.txt":["NumCl","NomCl","NumRuelCl","NomRueCl","CodePosteCl","VileCl"],
                    "DEFCLASSES.txt":["NumVol","Classe","CoefPrix"],
                    "PILOTES.txt":["Numpil","NomPil","NaisPil","VillePil"],
                    "RESERVATIONS.txt":["NumCl","NumVol","Classe","NbPlaces"],
                    "VOLS.txt":["NumVol","VilleD","VilleA" ,"DateD","HD time" ,"DateA","HA time" ,"NumPil" ,"NumAv"],
}

listFile=[] #on fait une liste des fichiers .txt
dirPilote = r"D:\Bdd_MEDANI_Lina\Redis"  
for file in os.listdir(dirPilote):
    if os.path.splitext(file)[1]==".txt":
        listFile.append(os.path.join(dirPilote,file))

dictAllJson={} #variable dictionnaire en json qui contiendra toute les données des fichiers txt
for fileName in listFile:         #on ouvre les fichiers txt 1 par 1
    name = os.path.basename(fileName)  #
    dictAllJson[name]={}          #
    with open(fileName) as fh:    #
        for line in fh: #Ligne par ligne

            description = list( line.strip().split("\t")) #On sépare chaque éléments de la ligne dans une liste


            dictAllJson[name][description[0]]={} #on prend le premier élément pour qu'il soit le nom du nouveau dictionnaire
            fields=tableCorespondance[name]      #On prend la bonne partie de tableCorrespondance du haut
            i=1
            for categorie in fields[1:]:         #pour chaque colonne du tableau
                dictAllJson[name][description[0]][categorie]=description[i] #on associe le nom de la colonne à sa valeur
                i+=1
###On a skip le i=0 car on l'utilise pour le nom du dico et donc on a déjà l'info, pas besoin de la remettre encore à l'intérieur

jsonFinal={} #json final après la fusion
print(json.dumps(dictAllJson["RESERVATIONS.txt"], indent=4))
idReserv = 0  # ID unique pour chaque réservation
idReserv = 0  # ID unique pour chaque réservation
for vol in dictAllJson["VOLS.txt"]:  # Itération sur chaque vol
    jsonFinal[vol] = dictAllJson["VOLS.txt"][vol]

    # Ajout des réservations pour le vol
    jsonFinal[vol]["reservations"] = {}

    for reserv in dictAllJson["RESERVATIONS.txt"]:
        print(f"Vérification de la réservation {reserv} pour le vol {vol}")
        if vol == dictAllJson["RESERVATIONS.txt"][reserv]["NumVol"]:
            print(f"Réservation {reserv} ajoutée pour le vol {vol}")
            jsonFinal[vol]["reservations"][str(idReserv)] = dictAllJson["RESERVATIONS.txt"][reserv]
            jsonFinal[vol]["reservations"][str(idReserv)]["NumCl"] = reserv

            # Ajout des détails du client
            for client in dictAllJson["CLIENTS.txt"]:
                if jsonFinal[vol]["reservations"][str(idReserv)]["NumCl"] == client:
                    print(f"Détails du client {client} ajoutés pour la réservation {idReserv}")
                    jsonFinal[vol]["reservations"][str(idReserv)]["client"] = dictAllJson["CLIENTS.txt"][client]

            del(jsonFinal[vol]["reservations"][str(idReserv)]["NumCl"])

            idReserv += 1  # Incrémenter l'ID de la réservation

pretty_json = json.dumps(jsonFinal, indent=4) #juste pour afficher de manière claire
print(pretty_json[0:1000],"......")
# Connexion à Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Stocker les données dans Redis pour chaque vol à partir de V101
for vol in jsonFinal:
    if int(vol[1:]) >= 101:  # On prend seulement les vols à partir de V101
        key = f"vol:{vol}"  # Créer une clé unique pour chaque vol
        json_data = json.dumps(jsonFinal[vol])  # Convertir le dictionnaire en JSON
        r.set(key, json_data)  # Stocker dans Redis
        print(f"Vol {vol} stocké dans Redis sous la clé {key}")

print("Les données des vols à partir de V101 ont été stockées dans Redis.")

keys = r.keys("vol:*")  # Récupérer toutes les clés qui commencent par "vol:"

# Afficher les vols stockés
for key in keys:
    vol_data = r.get(key)  # Récupérer les données pour chaque clé
    vol_json = json.loads(vol_data)  # Convertir la chaîne JSON en dictionnaire
    print(f"{key}: {json.dumps(vol_json, indent=4)}")  # Afficher les données
#lister toutes les villes d’arrivée 
def lister_villes_arrivee(ville_depart):
    r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    villes_arrivee = set()

    # Récupérer toutes les clés de vols
    keys = r.keys("vol:*")

    for key in keys:
        vol_data = r.get(key)  # Récupérer les données du vol
        vol_json = json.loads(vol_data)  # Convertir en dictionnaire

        # Vérifier si la ville de départ correspond
        if vol_json.get("VilleD") == ville_depart:
            villes_arrivee.add(vol_json.get("VilleA"))

    return list(villes_arrivee)

# Exemple d'utilisation
if __name__ == "__main__":
    ville = "Paris"  # Remplace par la ville que tu souhaites interroger
    villes = lister_villes_arrivee(ville)
    print(f"Villes d'arrivée pour {ville}: {villes}")
with open("data.json", "w") as fichier:
    json.dump(jsonFinal, fichier, indent=4)
print(pretty_json)
