import json 
import os
import random
import pygad
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

# gera a quantidade de ginasios aleatorio ou permite um valor fixo
def selecionar_ginasios(ginasios, quantidade):
    if quantidade == 0:
        return random.sample(ginasios, random.randint(1, len(ginasios)))
    return random.sample(ginasios, min(quantidade, len(ginasios)))

# verifica vantagem de tipo de pokemon pra pokemon e penaliza ou da beneficios
def vantagem(pokemon_time, pokemon_ginasio):
    if pokemon_ginasio in vantagens_forte_contra.get(pokemon_time, []):
        return 2 
    elif pokemon_time in vantagens_forte_contra.get(pokemon_ginasio, []):
        return 0.5
    else: 
        return 1

# calcula a vantage de tipo geral do time contra o time do ginasio   
def calcular_vantagem(pokemon_time, pokemon_ginasio):
    valor_total = 1
    for tipo_atk in pokemon_time.tipos:
        for tipo_def in pokemon_ginasio.tipos:
            valor_total *= vantagem(tipo_atk, tipo_def)
    return valor_total

# define o poder total do pokemon
def poder_pokemon(pokemon):
    atributos = pokemon.atributos
    return atributos["ataque"] + atributos["ataque_especial"] + atributos["velocidade"]

# logica para o ataque e defesa
def dano_recebido(pokemon_atacante, pokemon_defensor, multiplicador_vantagem):
    ataque = pokemon_atacante.atributos["ataque"] + pokemon_atacante.atributos["ataque_especial"]

    defesa = pokemon_defensor.atributos["defesa"] + pokemon_defensor.atributos["defesa_especial"]
    return (ataque / defesa) * multiplicador_vantagem * 100

# calcula o valor total de uma "batalha" de pokemon pra pokemon
def valor_total_batalha(pokemon_time, pokemon_ginasio):
    vantagem_de_tipo_time_gerado = calcular_vantagem(pokemon_time, pokemon_ginasio)

    vantagem_de_tipo_ginasio = calcular_vantagem(pokemon_ginasio, pokemon_time)

    poder_time_gerado = poder_pokemon(pokemon_time) * vantagem_de_tipo_time_gerado

    dano = dano_recebido(pokemon_ginasio, pokemon_time, vantagem_de_tipo_ginasio)

    pontos_de_vida_restante = pokemon_time.atributos["hp"] - dano

    if pontos_de_vida_restante <= 0:
        return -1000
    return poder_time_gerado + pontos_de_vida_restante

###################################################
#função que cria o time de pokemons baseado na solução do algoritmo genético
def criar_time(solucao, pokemons):
    time = []
    for gene in solucao:
        time.append(pokemons[gene])
    return time


# função que simula a batalha entre o time do jogador e o time do ginasio
def batalha(time, ginasio):
    pontos_time = 0
    
    for pokemon_time in time:
        melhor = 0
        for pokemon_inimigo in ginasio.pokemons:
            valor = valor_total_batalha(
                pokemon_time,
                pokemon_inimigo
            )
            if valor > melhor:
                melhor = valor
        pontos_time += melhor
    pontos_ginasio = 0

    for pokemon in ginasio.pokemons:
        pontos_ginasio += poder_pokemon(pokemon)

    return max(0, pontos_time - pontos_ginasio)

# função de fitness que será usada pelo algoritmo genético
def calcular_fitness(
        ga_instance,
        solucao,
        solucao_idx,
        pokemons,
        ginasios):
    
    time = criar_time(
        solucao,
        pokemons
    )

    pontuacao = 0
    for ginasio in ginasios:
        if batalha(time, ginasio):
            pontuacao += random.uniform(0, 5)

    return pontuacao
