from funcoes import *

def main(): 
    pokemons = carregar_pokemons()

    ginasios = carregar_ginasios()

    # debug 
    """
    for ginasio in ginasios:
        print(ginasio.nome, ginasio.tipo)
        for pokemon in ginasio.pokemons:
            print(" ", pokemon.nome, pokemon.tipos)
    """
    """
    for pokemon in pokemons:
    print(pokemon.nome, pokemon.tipos)
    for atributo, valor in pokemon.atributos.items():
        print(f"  {atributo}: {valor}")
    """
    quantidade = int(input("Quantos ginásios? (0 para aleatório, -1 para experimentos): "))

    if quantidade == 10:
        rodar_experimentos(pokemons, ginasios)
    #else:
        #ginasios_selecionados = selecionar_ginasios(ginasios, quantidade)

    #print("\nGinásios selecionados:")
    #for ginasio in ginasios_selecionados:
        #print(f"  {ginasio.nome} — {ginasio.tipo}")
    
    #time, fitness = executar_algoritmo_genetico(pokemons, ginasios_selecionados)

    """print("\nMelhor time gerado:")
    for pokemon in time:
        print(f"  {pokemon.nome} — {pokemon.tipos}")

    print(f"\nFitness: {fitness}")"""


    """for ginasio in ginasios_selecionados:
        tem_vantagem = any(
            vantagem(tipo, ginasio.tipo) == 2
            for p in time for tipo in p.tipos
        )
        if not tem_vantagem:
            print(f"  Sem cobertura: {ginasio.nome} ({ginasio.tipo})")"""

if __name__ == "__main__":
    main()