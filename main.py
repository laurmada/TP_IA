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
    quantidade = int(input("Quantos ginásios? (0 para aleatório): "))
    
    ginasios_selecionados = selecionar_ginasios(ginasios, quantidade)

if __name__ == "__main__":
    main()