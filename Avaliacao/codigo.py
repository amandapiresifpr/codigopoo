from Jogador import Jogador
from Equipe import Equipe

jogadores = []  #lista que armazena todos os jogadores
equipes = []  # lista que armazena todas as equipes

while True:  #repeticao faz o menu rodar
    print("========================================")
    print(" CAMPEONATO INTERCLASSE DE E-SPORTS ")
    print("========================================")
    print("1. Cadastrar jogador")
    print("2. Cadastrar equipe")
    print("3. Adicionar jogador a uma equipe")
    print("4. Listar todas as equipes")
    print("5. Listar jogadores de uma equipe")
    print("6. Buscar jogador por nickname")
    print("0. Sair")
    print("========================================")

    op = input("Escolha uma opção: ")  # le  opção digitada pelo usuário

    if op == "1":
        nome = input("Nome: ")  # pede o nome
        nick = input("Nickname: ")  # pede o nickname
        turma = input("Turma: ")  # pede a turma
        jogadores.append(Jogador(nome, nick, turma))  # cria jogador e adiciona na lista
        print("Jogador cadastrado!")  # confirma cadastro

    elif op == "2":
        nome = input("Nome da equipe: ")  #pede nome da equipe
        jogo = input("Jogo: ")  # pede o jogo
        equipes.append(Equipe(nome, jogo))  # cria equipe e adiciona na lista nofim
        print("Equipe cadastrada!")  #confirma cadastro

    elif op == "3":
        i = 0
        for j in jogadores:  #percorre lista de jogadores
            print(i + 1, "-", j)  # mostra jogador com número
            i = i + 1  # incrementa o contador

        jg = int(input("Escolha jogador: ")) - 1  # usuaio escolhe jogador pelo indice

        i = 0
        for e in equipes:  # percorre lista de equipes
            print(i + 1, "-", e)  # mostra equipe com número
            i = i + 1  # incrementa o contador

        eq = int(input("Escolha equipe: ")) - 1  # usuario escolhe equipe pelo indice tb

        equipes[eq].adicionar_jogador(jogadores[jg])  # adiciona jogador na equipe
        print("Adicionado!")  

    elif op == "4":
        for e in equipes:  # percorre todas as equipes
            print(e, "| Jogadores:", len(e.jogadores))  # mostra equipe e quantidade de jogadores

    elif op == "5":
        i = 0
        for e in equipes:  # lista equipes
            print(i + 1, "-", e)
            i = i + 1

        eq = int(input("Escolha equipe: ")) - 1  #escolhe equipe
        equipes[eq].listar_jogadores()  # mostra jogadores da equipe

    elif op == "6":
        busca = input("Nickname: ")  #pede nick
        for j in jogadores:  # percorre lista de jogadores
            if j.nickname == busca:  # verifica se encontrou
                print(j)  # mostra jogador

    elif op == "0":
        break  
    else:
        print("Opção inválida")  