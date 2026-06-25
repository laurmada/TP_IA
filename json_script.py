import requests
import json

def gerar_pokemon(id):
    url = f"https://pokeapi.co/api/v2/pokemon/{id}"
    data = requests.get(url).json()

    return {
        "id": id,
        "nome": data["name"],
        "tipos": [t["type"]["name"] for t in data["types"]],
        "atributos": {
            "hp": data["stats"][0]["base_stat"],
            "ataque": data["stats"][1]["base_stat"],
            "defesa": data["stats"][2]["base_stat"],
            "ataque_especial": data["stats"][3]["base_stat"],
            "defesa_especial": data["stats"][4]["base_stat"],
            "velocidade": data["stats"][5]["base_stat"]
        }
    }

pokemons = []

for i in range(1, 152):  
    print(f"Buscando Pokémon {i}")
    pokemons.append(gerar_pokemon(i))

with open("pokemons.json", "w", encoding="utf-8") as f:
    json.dump(pokemons, f, indent=2, ensure_ascii=False)

print("JSON criado com sucesso!")