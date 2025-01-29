import redis
import json
import time

# Charger json_final depuis un fichier JSON 
with open('vols_final.json', 'r') as json_file:
    json_final = json.load(json_file)

# Connexion à Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
# Mesurer le temps d'insertion
start_time = time.time()
# Stocker chaque vol dans Redis
for vol_id, vol_data in json_final.items():
    r.set(f"vol:{vol_id}", json.dumps(vol_data))
insertion_time = time.time() - start_time
print(f"Temps d'insertion dans Redis : {insertion_time:.4f} secondes")
    
# Mesurer le temps de lecture
start_time = time.time()
for vol_id in json_final.keys():
    r.get(f"vol:{vol_id}")
reading_time = time.time() - start_time
print(f"Temps de lecture dans Redis : {reading_time:.4f} secondes")
