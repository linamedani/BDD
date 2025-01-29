import json
import os

# Chemin du fichier JSON à lire
input_file = 'vols_final.json'

# Lire le contenu du fichier JSON
with open(input_file, 'r') as f:
    vols_final = json.load(f)

# Diviser le JSON final
keys = list(vols_final.keys())
midpoint = len(keys) // 2
vols_part1 = {k: vols_final[k] for k in keys[:midpoint]}
vols_part2 = {k: vols_final[k] for k in keys[midpoint:]}

# Créer un dossier pour stocker les fichiers JSON 
output_dir = "D:\\Bdd_MEDANI_Lina\\Mongo"  

# Sauvegarder en tant que fichiers JSON
part1_path = os.path.join(output_dir, 'vols_part1.json')
part2_path = os.path.join(output_dir, 'vols_part2.json')

# Ouvrir et écrire les fichiers
with open(part1_path, 'w') as f1, open(part2_path, 'w') as f2:
    json.dump(vols_part1, f1, indent=4)
    json.dump(vols_part2, f2, indent=4)

print("Les fichiers JSON ont été sauvegardés dans le dossier :", output_dir)
