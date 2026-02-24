print("Programação Orientada a Objetos")

"""nome = input("Nome: ")
idade = input("Idade: ")
idade = int(idade)
salario = float(input("Salário: R$ "))

# str formatada
print(f"Olá, {nome}. Você tem {idade} anos.")

if(salario <= 10000):
    print(f"Você ganha muito mal: R${salario:.2f}")
elif(salario > 10000 and salario <= 15000):
    print(f"Você ganha bem: R${salario:.2f}")
else:
    print(f"Você ganha muito bem: R${salario:.2f}")
    """

#num = int(input("Digite um número "))
#EXERCICIO 1
"""
if(num > 100):
    print(num/2)
    """
#EXERCICIO 2
"""
if(num % 2 == 0):
    print("O número é par")
else:
    print("O número é ímpar")
"""
#EXERCICIO 3
num1 = int(input("Digite o primeiro número: "))
num2 = int(input("Digite o segundo número: "))
op = str(input("Digite um operador matemático (*, /, +, -)"))

if(op == "*"):
    print("O resultado é", num1 * num2)
elif(op == "/"):
    print("O resultado é", num1 / num2)
elif(op == "+"):
    print("O resultado é", num1 + num2)
elif(op == "-"):
    print("O resultado é", num1 - num2)
else:
    ("Operador inválido")