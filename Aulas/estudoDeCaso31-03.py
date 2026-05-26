class Conta:

    def __iniit__(self):
        self.id = ""
        self.titular = ""
        self.saldo = 0
    
    def depositar(self):
        valorDep = float(input("Digite o valor a ser depositado"))
        self.saldo += valorDep


    def sacar(self):
        pass

    def transferir(self):
        pass


conta1 = Conta(1)
conta1.id = 1
conta1.titular = "João"
conta1.saldo = 1000

conta2 = Conta(2)
conta2.id = 2
conta2.titular = "Maria"
conta2.saldo = 500