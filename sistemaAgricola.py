op = 0
while(op != 4):
    print("""1 - Cadastrar Produto
    2 - Listar Produtos
    3 - Aplicar Desconto
    4 - Sair do Programa""")
    op = int(input("Digite um número de 1 a 4 para escolher uma opção: "))
    if(op == 1):
        print("1 - Cadastrar Produto")
    elif(op == 2):
        print("2 - Listar Produtos")
    elif(op == 3):
        print("3 - Aplicar Desconto")
    elif(op == 4):
        print("4 - Sair do Programa")
    else:
        print("Opção inválida, digite novamente")