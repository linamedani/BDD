import json

# Chemins des fichiers JSON à lire
part1_path = 'D:\\Bdd_MEDANI_Lina\\Mongo\\vols_part1.json'
part2_path = 'D:\\Bdd_MEDANI_Lina\\Mongo\\vols_part2.json'

# Charger vols_part1.json et vols_part2.json
with open(part1_path, 'r') as f1, open(part2_path, 'r') as f2:
    vols_part1 = json.load(f1)
    vols_part2 = json.load(f2)



# Jointure et sauvegarde des résultats
def jointure(d1, d2, att):
    resultats_jointure = []  # Liste pour stocker les résultats de jointure
    for i in d1.keys():
        for j in d2.keys():
            if d1[i].get(att) == d2[j].get(att):
                resultat = {
                    'vol_part1': d1[i],
                    'vol_part2': d2[j],
                }
                resultats_jointure.append(resultat)
    return resultats_jointure

# Exécuter la jointure sur l'attribut 'Numvol'
resultats = jointure(vols_part1, vols_part2, 'Numvol')

# Sauvegarder les résultats dans un fichier JSON
output_file = 'D:\\Bdd_MEDANI_Lina\\Mongo\\vols_jointure.json'
with open(output_file, 'w') as f_output:
    json.dump(resultats, f_output, indent=4)

print(f"Les résultats de la jointure ont été sauvegardés dans le fichier : {output_file}")
