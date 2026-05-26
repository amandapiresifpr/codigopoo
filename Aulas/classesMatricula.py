class Campus:
    # Método construtor é obrigatório
    # Todo método deve ter o parâmetro "self"
    def __init__(self):
        #self acessa os atributos do objeto
        self.nome_campus = ""
        self.endereco = ""

    # Método usado ao "imprimir" um objeto
    def __str__(self):
        return f"Campus: {self.nome_campus}"

# Criação da Classe Aluno
class Aluno:
    def __init__(self, nome):
        self.nome_aluno = nome
        self.email_aluno = ""
        self.cpf_aluno = ""
        self.telefone_aluno = ""
        self.data_nasc = ""
    
    def __str__(self):
        return f"Aluno: {self.nome_aluno}"
    # Criar um métido para apresentar o Aluno
    def apresentar(self):
        print(f"O (a) {self.nome_aluno} nasceu em {self.data_nasc}")
        if(self.cpf_aluno == ""):
            print("O (a) aluno não cadastrou CPF.")
        else: 
            print("CPF:", self.cpf_aluno[0:3], "...")

    #Criação dos objetos
 
# nome_do_objeto = Classe_do_objeto()
# nome_do_objeto = atributo1 = "Valor"
# nome_do_objeto = atributo2 = "Valor 2"
# nome_do_objeto = atributo3 = 199.90
# nome_do_objeto.metodo1()
# nome_do_objeto.metodo2()

#Criar um objeto para a aluna "Amanda"
amanda = Aluno("Amanda")
# amanda.nome_aluno = "Amanda"
amanda.email_aluno = "20241pvai0030034@estudantes.ifpr.edu.br"
amanda.cpf_aluno = "098.613.049-40"
amanda.telefone_aluno = "44999908849"
amanda.data_nasc = "05/03/2009"
amanda.apresentar()

felipe = Aluno("Felipe")
felipe.email_aluno = "20241pvai0030007@estudantes.ifpr.edu.br"
felipe.cpf_aluno = "149.963.279-79"
felipe.telefone_aluno = "44997034595"
felipe.data_nasc = "25/01/2009"
felipe.apresentar()