class Pokemon:
    def __init__(
        self,
        id,
        nome,
        tipos,
        atributos,
    ):

        self.id = id
        self.nome = nome
        self.tipos = tipos
        self.atributos = atributos

    
class Ginasio:
    def __init__(
        self,
        id,
        nome,
        tipo,
        pokemons,
    ):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.pokemons = pokemons