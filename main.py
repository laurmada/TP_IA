from funcoes import *
import time as time_module

def main(): 
    # carrega json dos pokemons e times
    pokemons = carregar_pokemons()
    ginasios = carregar_ginasios()

    quantidade = int(input("Quantos ginásios? (0 para aleatório: "))

    ginasios_selecionados = selecionar_ginasios(ginasios, quantidade)

    print("\nGinásios selecionados:")
    for ginasio in ginasios_selecionados:
        print(f"  {ginasio.nome} — {ginasio.tipo}")

    # chama o algoritmo genetico com a quantidade de ginasios selecionados e lista de pokemons 
    melhor_time, fitness = executar_algoritmo_genetico(pokemons, ginasios_selecionados)

    print("\nMelhor time gerado:")
    for pokemon in melhor_time:
        print(f"  {pokemon.nome} — {pokemon.tipos}")

    print(f"\nFitness: {fitness}")

    for ginasio in ginasios_selecionados:
        tem_vantagem = any(
            vantagem(tipo, ginasio.tipo) == 2
            for p in melhor_time for tipo in p.tipos
        )
        if not tem_vantagem:
            print(f"  Sem cobertura: {ginasio.nome} ({ginasio.tipo})")

if __name__ == "__main__":
    main()