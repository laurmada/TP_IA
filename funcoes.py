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

# definine uma metrica para definir vitoria, empate ou derrota
def resultado_provavel(score_time, score_ginasio):
    razao_metrica = score_time / score_ginasio if score_ginasio > 0 else 1
    if razao_metrica >= 1.05:
        return "Vitória"
    elif razao_metrica >= 0.95:
        return "Empate"
    else:
        return "Derrota"

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
    for tipo_ataque in pokemon_time.tipos:
        for tipo_defesa in pokemon_ginasio.tipos:
            valor_total *= vantagem(tipo_ataque, tipo_defesa)
    return valor_total

# define um bonus por cobertura de tipo 
def bonus_cobertura(time, ginasios):
    cobertura = 0

    for ginasio in ginasios:
        for pokemon_ginasio in ginasio.pokemons:
            for pokemon_gerado in time:
                if calcular_vantagem(pokemon_gerado, pokemon_ginasio) > 1:
                    cobertura += 1
                    break
    return cobertura * 500

# define o poder total do pokemon
def poder_pokemon(pokemon):
    atributos = pokemon.atributos
    return atributos["ataque"] + atributos["ataque_especial"] + atributos["velocidade"]

# logica para o ataque e defesa
def dano_recebido(pokemon_atacante, pokemon_defensor, multiplicador_vantagem):
    ataque = pokemon_atacante.atributos["ataque"] + pokemon_atacante.atributos["ataque_especial"]

    defesa = pokemon_defensor.atributos["defesa"] + pokemon_defensor.atributos["defesa_especial"]
    return (ataque / defesa) * multiplicador_vantagem 

# calcula o valor total de uma "batalha" de pokemon pra pokemon
def valor_total_batalha(pokemon_time, pokemon_ginasio):
    vantagem_de_tipo_time_gerado = calcular_vantagem(pokemon_time, pokemon_ginasio)

    vantagem_de_tipo_ginasio = calcular_vantagem(pokemon_ginasio, pokemon_time)

    poder_time_gerado = poder_pokemon(pokemon_time) * vantagem_de_tipo_time_gerado * 2

    dano = dano_recebido(pokemon_ginasio, pokemon_time, vantagem_de_tipo_ginasio)

    pontos_de_vida_restante = pokemon_time.atributos["pontos_de_vida"] - dano

    return poder_time_gerado + pontos_de_vida_restante

# penalidade para evitar pokemos lendarios que sao mais fortes
def penalidade_lendarios(time):
    lendarios = {"mewtwo", "mew", "articuno", "zapdos", "moltres"}
    contador = sum(1 for p in time if p.nome in lendarios)
    return contador * 2000

# calcula o score total do time gerado contra um ginasio especifico
def score_time_vs_ginasio(time, ginasio):
    score_total = 0
    quantidade_inimigos = len(ginasio.pokemons)

    for pokemon_ginasio in ginasio.pokemons:
        for pokemon_time_gerado in time:
            score_combate = valor_total_batalha(pokemon_time_gerado, pokemon_ginasio)
            score_total += score_combate

    return score_total / quantidade_inimigos

# calcula o poder total do ginasio da mesma forma q foi calculado para o time
def poder_total_ginasio(time, ginasio):
    score_total = 0
    quantidade_pokemons_time = len(time)

    for pokemon_ginasio in ginasio.pokemons:
        for pokemon_gerado in time:
            vantagem_ginasio = calcular_vantagem(pokemon_ginasio, pokemon_gerado)
            vantagem_time = calcular_vantagem(pokemon_gerado, pokemon_ginasio)
            # * 2 para o ataque ter um peso maior que os pontos de vida do pokemon
            poder_ginasio = poder_pokemon(pokemon_ginasio) * vantagem_ginasio * 2
            dano_no_ginasio = dano_recebido(pokemon_gerado, pokemon_ginasio, vantagem_time)
            hp_ginasio_restante = pokemon_ginasio.atributos["pontos_de_vida"] - dano_no_ginasio

            if hp_ginasio_restante <= 0:
                score_total += -1000
            else:
                score_total += poder_ginasio + hp_ginasio_restante

    return score_total / quantidade_pokemons_time

# funcao que executa o algoritmo genetico 
def executar_algoritmo_genetico(pokemons, ginasios):
    # funcao q define o fitness do algoritmo genetico
    def fitness_func(ga_instance, solution, solution_idx):
        time = [pokemons[i] for i in solution]
        score_total = 0.0

        for ginasio in ginasios:
            score_time_gerado = score_time_vs_ginasio(time, ginasio)
            score_total += score_time_gerado

        score_total += bonus_cobertura(time, ginasios)
        score_total -= penalidade_lendarios(time)

        return float(score_total)

    # configuracao do algoritmo genetico usando a biblioteca pygad
    ga = pygad.GA(
        num_generations=80,
        num_parents_mating=5,
        fitness_func=fitness_func,
        sol_per_pop=50,
        num_genes=6,
        gene_type=int,
        gene_space=range(0, len(pokemons)),
        allow_duplicate_genes=False,
        mutation_num_genes=2,
    )

    ga.run()
    solution, fitness, _ = ga.best_solution()
    melhor_time = [pokemons[i] for i in solution]

    '''print(" DEBUG DO MELHOR TIME ENCONTRADO")
    for i, p in enumerate(melhor_time, 1):
        print(f"  {i}. {p.nome} - Tipos: {p.tipos}")

    for ginasio in ginasios:
        score_time = score_time_vs_ginasio(melhor_time, ginasio)
        score_ginasio = poder_total_ginasio(melhor_time, ginasio)

        if score_time == -1000:
            print(f" Ginásio {ginasio.nome} ({ginasio.tipo}): DERROTA!")
        else:
            resultado = resultado_provavel(score_time, score_ginasio)
            print(f" Ginásio {ginasio.nome} ({ginasio.tipo}): {resultado}")
            print(f"   Score do time: {score_time:.2f} | Score do ginásio: {score_ginasio:.2f}")

    valor_cobertura = bonus_cobertura(melhor_time, ginasios)
    valor_lendarios = penalidade_lendarios(melhor_time)

    print(" RESUMO DE BONUS E PENALIDADES:")
    print(f" Bônus de Cobertura de Tipos:  +{valor_cobertura}")
    print(f" Penalidade de Lendários:     -{valor_lendarios}")'''

    return melhor_time, fitness
