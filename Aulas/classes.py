class Animal:
    def __init__(self, nome, especie, patas):
        self.nome = nome
        self.especie = especie
        self.patas = patas

    def respirar(self):
        print("Respirando...")

    def rugir(self):
        print("O animal vai rugir!!")

class Gato(Animal):
    def __init__(self, nome, especie, patas, dono):
        super().__init__(nome, especie, patas)
        self.dono = dono

    def ronronar(self):
        print("Ronronando... miau")

    def rugir(self):
        super().rugir()
        print("miauuuuu miauu rrrawn")

class Cachorro(Animal):
    def abanar_rabo(self):
        print("Abanando rabo!!!")

    def rugir(self):
        print("auuu auuuuauu rãrrrrr")

                               