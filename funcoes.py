import json 
import os
from modelos import Pokemon, Ginasio

# dicionario para deteminar quais pokemons sao fortes contra quais
vantagens_forte_contra = {
    "normal": [],
    "fogo": ["grama", "gelo", "inseto", "aco"],
    "agua": ["fogo", "terra", "pedra"],
    "eletrico": ["agua", "voador"],
    "grama": ["agua", "terra", "pedra"],
    "gelo": ["grama", "terra", "voador", "dragao"],
    "lutador": ["normal", "gelo", "pedra", "noturno", "aco"],
    "venenoso": ["grama", "fada"],
    "terra": ["fogo", "eletrico", "venenoso", "pedra", "aco"],
    "voador": ["grama", "lutador", "inseto"],
    "psiquico": ["lutador", "venenoso"],
    "inseto": ["grama", "psiquico", "noturno"],
    "pedra": ["fogo", "gelo", "voador", "inseto"],
    "fantasma": ["psiquico", "fantasma"],
    "dragao": ["dragao"],
    "aco": ["gelo", "pedra", "fada"],
    "fada": ["lutador", "dragao", "noturno"]
}

# verifica vantagem de tipo de pokemon pra pokemn
def vantagem(pokemon_time, pokemon_ginasio):
    if pokemon_ginasio in vantagens_forte_contra.get(pokemon_time, []):
        return 2 
    elif pokemon_time in vantagens_forte_contra.get(pokemon_ginasio, []):
        return 0.5
    else: 
        return 1

# calcula a vantage de tipo geral do time contra o time do ginasio   
def calcular_vantagem(pokemon_time, pokemon_ginasio):
    multiplicador = 1
    for tipo_atk in pokemon_time.tipos:
        for tipo_def in pokemon_ginasio.tipos:
            multiplicador *= vantagem(tipo_atk, tipo_def)
    return multiplicador

# carrega o json dos pokemons e armazena em uma lista
def carregar_pokemons():
    caminho = os.path.join(os.path.dirname(__file__), "dados", "pokemons.json")
    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    pokemons = []

    for i in dados:
        pokemons.append(
            Pokemon(
                id=i["id"],
                nome=i["nome"],
                tipos=i["tipos"],
                atributos=i["atributos"]
            )
        )

    return pokemons

# carrega o json dos ginasios e armazena em uma lista 
def carregar_ginasios():
    caminho = os.path.join(os.path.dirname(__file__), "dados", "ginasios.json")
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    ginasios = []

    for j in dados:
        pokemons = []

        for i in j["pokemons"]:
            pokemons.append(Pokemon(
                i["id"],
                i["nome"],
                i["tipos"],
                i["atributos"]
            ))

        ginasio = Ginasio(
            j["id"],
            j["nome"],
            j["tipo"],
            pokemons
        )

        ginasios.append(ginasio)

    return ginasios


