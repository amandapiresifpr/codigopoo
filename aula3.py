import random
#EXERCICIO 1 - RANDOM E WHILE
""""
num = 0
while(num < 10 or num > 15):
    num = int(input("Digite um número entre 10 e 15"))

sort = random.randint(10, 15)

if (sort == num):
    print("Você acertou o valor!", sort)
else:
    print("Você errou o valor!", sort)
"""

#EXERCICIO 2 - RANDOM E WHILE
"""
num = 0
while(num < 10 or num > 15):
    num = int(input("Digite um número entre 10 e 15"))

sort = random.randint(10, 15)

while (sort != num):
    num = int(input("Você errou o valor, tente novamente!"))
print("Você acertou o valor!")
"""

#EXERCICIO 3 - FOR

for i in range(1, 10 + 1):
    print(i)