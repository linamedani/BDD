import json

# Charger doc1.json et doc2.json
with open('doc1.json', 'r') as f1, open('doc2.json', 'r') as f2:
    doc1 = json.load(f1)
    doc2 = json.load(f2)

# Afficher les contenus pour vérification
print("Contenu de doc1:", json.dumps(doc1, indent=2))
print("Contenu de doc2:", json.dumps(doc2, indent=2))

# Vérifiez si 'Numvol' existe dans les deux documents
missing_in_doc1 = []
missing_in_doc2 = []

for key, value in doc1.items():
    if 'Numvol' not in value:
        missing_in_doc1.append(key)

for key, value in doc2.items():
    if 'Numvol' not in value:
        missing_in_doc2.append(key)

# Jointure et sauvegarde des résultats
def jointure(d1, d2, att):
    resultats_jointure = []  # Liste pour stocker les résultats de jointure
    for i in d1.keys():
        for j in d2.keys():
            if d1[i].get(att) == d2[j].get(att):
                resultat = {
                    'doc1': d1[i],
                    'doc2': d2[j],
                }
                resultats_jointure.append(resultat)

    return resultats_jointure

# Exécuter la jointure sur l'attribut 'Numvol'
resultats = jointure(doc1, doc2, 'Numvol')

# Sauvegarder les résultats dans un fichier JSON
output_file = 'resultats_jointure.json'
with open(output_file, 'w') as f_output:
    json.dump(resultats, f_output, indent=4)

print(f"Les résultats de la jointure ont été sauvegardés dans le fichier : {output_file}")
