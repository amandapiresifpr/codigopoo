import math

class Calculadora:
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano

    def somar(self, a, b, c=0):
        result = a + b
        return result
    
    def subtrair(self, a, b, c=0):
        result = a - b
        return result
    
    def multiplicar(self, a, b, c=1):
        result = a * b
        return result
    
    def dividir(self, a, b, c=1):
        if(a == 0 or b == 0):
            print("Não é possível realizar a divisão")
        result = a / b
        return result
    
class CalculadoraCientifica (Calculadora):
    def __init__(self, marca, modelo, ano):
        super().__init__(marca, modelo, ano)
        self.funcoes_cientificas = "Existem 2 funções disponíveis, potenciação e realização de raiz quadrada"

    def potencia(self, a, b):
        result = a ** b
        return result
    
    def raiz_quadrada(self, a):
        result = math.sqrt(a)
        return result