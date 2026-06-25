from funcoes import carregar_ginasios, carregar_pokemons

def main(): 
    pokemons = carregar_pokemons()

    ginasios = carregar_ginasios()

    for ginasio in ginasios:
        print(ginasio.nome, ginasio.tipo)
        for pokemon in ginasio.pokemons:
            print(" ", pokemon.nome, pokemon.tipos)
    
if __name__ == "__main__":
    main()