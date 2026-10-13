import os

print("Configurando email...✅")
email = "20241pvai0030034@estudantes.ifpr.edu.br"
os.system(f'git config user.email "{email}"')

print("Adicionando modificações...✅")
os.system("git add .")

mensagem = input("Mensagem do commit: ")
while len(mensagem) < 4:
    print("😢 Mensagem muito pequena, detalhe mais")
    mensagem = input("Digite novamente 😘: ")

print("Registrando alterações...✅")
os.system(f'git commit -m "{mensagem}"')

print("Enviando alterações...✅")
os.system("git push")
