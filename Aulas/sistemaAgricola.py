def calc_desconto(precos, desconto):
    for i in range(0, len(precos)):
        valor = precos[i]
        result = valor - (valor * (desconto/100))
        precos[i] = result
    return precos

indiceProd = 0
nomes = [""] * 10
precos = []

op = 0
while(op != 4):
    print("""1 - Cadastrar Produto
    2 - Listar Produtos
    3 - Aplicar Desconto
    4 - Sair do Programa""")
    op = int(input("Digite um número de 1 a 4 para escolher uma opção: "))

    if(op == 1):
        print("Cadastrar Produto")
        nome = str(input("Digite o nome do produto"))
        preco = float(input("Preço: R$ "))
        nomes[indiceProd] = nome
        indiceProd += 1
        precos.append(preco)

    elif(op == 2):
        print("Listar Produtos")
        for i in range(0, len(precos)):
            print(nomes[i], " - ", precos[i])

    elif(op == 3):
        print("Aplicar Desconto")
        desconto = int(input("Digite a porcentagem do desconto"))
        precos = calc_desconto(precos, desconto)
        for i in range(0, len(precos)):
            print(nomes[i], "-", precos[i])

    elif(op == 4):
        print("Sair do Programa")

    else:
        print("Opção inválida, digite novamente")
