class Jogador:
    def __init__(self, nome, nickname, turma):
        self.nome = nome  # atributo que guarda o nome
        self.nickname = nickname  # atributo que guarda o apelido
        self.turma = turma  # atributo que guarda a turma

    def __str__(self):
        return f"{self.nome} ({self.nickname}) - {self.turma}"  # define como o objeto aparece no print