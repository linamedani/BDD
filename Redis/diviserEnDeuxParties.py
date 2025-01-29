import json

def diviser_json_en_deux(data):
    keys = list(data.keys())
    mid = len(keys) // 2
    doc1 = {key: data[key] for key in keys[:mid]}
    doc2 = {key: data[key] for key in keys[mid:]}
    return doc1, doc2

# Charger json_final depuis le fichier
with open('vols_final.json', 'r') as json_file:
    json_final = json.load(json_file)

# Diviser json_final en deux documents
doc1, doc2 = diviser_json_en_deux(json_final)

# Enregistrer chaque document dans un fichier JSON séparé
with open('doc1.json', 'w') as file1:
    json.dump(doc1, file1, indent=4)

with open('doc2.json', 'w') as file2:
    json.dump(doc2, file2, indent=4)

print("Les fichiers 'doc1.json' et 'doc2.json' ont été créés avec succès.")

