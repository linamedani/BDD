import redis
import json

# Connexion à Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Lister toutes les clés
keys = r.keys('*')
print("Clés dans Redis:", keys)

# Afficher la valeur de chaque clé
for key in keys:
    value = r.get(key)
    print(f"{key}: {value}")

# Pour les clés de type hachage
for key in keys:
    if r.type(key) == 'hash':
        value = r.hgetall(key)
        print(f"{key}: {json.dumps(value, indent=2)}")
