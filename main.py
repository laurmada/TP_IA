from funcoes import *
from genetic_algorithm import criar_algoritmo_genetico
import matplotlib.pyplot as plt

def main(): 

    pokemons = carregar_pokemons()
    ginasios = carregar_ginasios()

    quantidade = int(
        input("Quantos ginásios? (0 para aleatório): ")
    )

    ginasios_selecionados = selecionar_ginasios(
        ginasios,
        quantidade
    )

    print("\nGinásios selecionados:")

    for ginasio in ginasios_selecionados:
        print(
            f"  {ginasio.nome} — {ginasio.tipo}"
        )

    # cria o algoritmo genético
    ga = criar_algoritmo_genetico(
        pokemons,
        ginasios_selecionados
    )

    # inicia evolução
    ga.run()

    # pega melhor solução encontrada
    melhor, fitness, indice = ga.best_solution()

    print("\nMelhor time encontrado:")

    for gene in melhor:
        print(pokemons[gene].nome)

    print("\nPontuação:", fitness)

    ga.plot_fitness()

if __name__ == "__main__":
    main()