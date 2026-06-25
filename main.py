from funcoes import carregar_ginasios, carregar_pokemons

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

if __name__ == "__main__":
    main()