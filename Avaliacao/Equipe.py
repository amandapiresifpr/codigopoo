class Equipe:
    def __init__(self, nome, jogo):
        self.nome = nome  # nome da equipe
        self.jogo = jogo  # jogo da equipe
        self.jogadores = []  # lista que vai armazenar jogadores

    def adicionar_jogador(self, jogador):
        self.jogadores.append(jogador)  # append adiciona um item no final da lista

    def listar_jogadores(self):
        for j in self.jogadores:  # percorre cada jogador dentro da lista jogadores
            print("-", j)  # imprime cada jogador

    def __str__(self):
        return f"{self.nome} ({self.jogo})"  # representação da equipe