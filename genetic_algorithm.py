import pygad

from funcoes import calcular_fitness


def criar_algoritmo_genetico(pokemons, ginasios):

    ga = pygad.GA(

    num_generations=100,

    sol_per_pop=50,

    num_parents_mating=10,

    num_genes=6,

    gene_type=int,

    gene_space=range(len(pokemons)),

    allow_duplicate_genes=False,

    mutation_type="random",

    mutation_percent_genes=30,

    fitness_func=lambda ga, solucao, indice:
        calcular_fitness(
            ga,
            solucao,
            indice,
            pokemons,
            ginasios
        )
    )

    return ga