from classes import Calculadora, CalculadoraCientifica

# Informando dados da calculadora
calc = Calculadora("", "", 0)
calc.marca = str(input("Digite a marca da calculadora"))
calc.modelo = str(input("Digite o modelo da calculadora"))
calc.ano = int(input("Digite o ano da calculadora"))
print(f"A calculadora é a {calc.modelo} da marca {calc.marca}, do ano de {calc.ano}")

numA = int(input("Informe um número inteiro para realizar as operações"))
numB = int(input("Informe o segundo número inteiro"))

print(f"""O resultado da soma {numA} + {numB} é {calc.somar(numA, numB)}
O resultado da subtração {numA} - {numB} é {calc.subtrair(numA, numB)}
O resultado da multiplicação de {numA} x {numB} é {calc.multiplicar(numA, numB)}
O resultado da divisão de {numA} / {numB} é {calc.dividir(numA, numB)}""")

calcCientifica = CalculadoraCientifica("", "", 0)
num = int(input("Informe um número inteiro para calcularmos as operações"))
print(f"""Esse número ao cubo é igual a {calcCientifica.potencia(num, 3)}
e a raíz quadrada dele é {calcCientifica.raiz_quadrada(num)}""")