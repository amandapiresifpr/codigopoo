
def verifica_par(x):
  
  if(x % 2 == 0):
    return True
  else:
    return False
    
x = int (input("Digite um numero inteiro "))
if(verifica_par(x)):
    print(f"O {x} é par")
else:
   print(f"O {x} é ímpar")


