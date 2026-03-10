import os

print("Configurando email...✅")
email = "20241pvai0030034@estudantes.ifpr.edu.br"
comando_email = 'git config user.email \"{email} "'
os.system(comando_email)

print("Adicionando modificações...✅")
comando1 = "git add *"
os.system(comando1)

mensagem = input("Mensagem do commit: ")
while(len(mensagem) < 4 ):
    print("😢 Mensagem muito pequena, detalhe mais")
    mensagem = input("DIigite novamente 😘")

print("Registrando alterações...✅")
comando2 = f'git commit -m "{mensagem}"'
os.system(comando2)

print("Enviando alterações...✅")
comando3 = "git push"
os.system(comando3)
