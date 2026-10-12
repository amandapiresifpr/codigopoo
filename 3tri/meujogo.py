import os
import random

import arcade

# Tudo o que é banco de dados mora em banco.py
from banco import db, Pontuacao, inicializar_banco

# ==========================================
# CONSTANTES GLOBAIS
# ==========================================
ALTURA = 600
LARGURA = 800
NOME = "Moranguinho"

VELOCIDADE = 4                      # Velocidade horizontal do jogador
VELOCIDADE_INIMIGO_ESPECIAL = 1.2   # Velocidade da bruxa perseguidora
GRAVIDADE = 0.5                     # gravity_constant do motor de física
FORCA_PULO = 16                     # change_y aplicado ao pular

TAMANHO_BLOCO = 75                  # bloco.png tem 75x75 px
TOPO_CHAO = TAMANHO_BLOCO           # Y do topo do chão (uma fileira de blocos)

ESCALA_PLAYER = 0.7                 # Quadros da jogadora têm 100x110 px
LIMITE_NOME = 12                    # Máximo de letras no nome do ranking

ARQUIVO_FUNDO = "fundo.png"
ARQUIVO_SPRITESHEET = "player_direita.png"

# Plataformas suspensas: (x do primeiro bloco, y do centro, quantidade de blocos)
PLATAFORMAS = [
    (75, 200, 3),
    (575, 200, 3),
    (325, 340, 3),
]

# Integrantes do grupo: (nome, arquivo do avatar).
# TROQUE pelos nomes reais e coloque as imagens na pasta do jogo.
AUTORES = [
    ("Amanda", "avatar_amanda.png"),
    ("Integrante 2", "avatar_2.png"),
]


# ==========================================
# CLASSES DAS ENTIDADES (todas herdam de arcade.Sprite)
# ==========================================
class Bloco(arcade.Sprite):
    """Bloco sólido usado como chão e como plataforma suspensa."""

    def __init__(self, x: float, y: float):
        super().__init__("bloco.png", scale=1)
        self.center_x = x
        self.center_y = y


class Player(arcade.Sprite):
    """
    Jogadora controlada pelo teclado.
    A física (gravidade/colisão) é do PhysicsEnginePlatformer; aqui só
    cuidamos da animação, usando uma máquina de estados.
    """

    def __init__(self):
        # 1. Carrega a folha de sprites e fatia em 4 quadros de 100x110 px
        folha = arcade.load_spritesheet(ARQUIVO_SPRITESHEET)
        quadros_direita = folha.get_texture_grid(
            size=(100, 110),
            columns=4,
            count=4
        )

        # 2. Versão espelhada de cada quadro, para andar para a esquerda
        quadros_esquerda = []
        for quadro in quadros_direita:
            quadros_esquerda.append(quadro.flip_left_right())

        super().__init__(quadros_direita[0], scale=ESCALA_PLAYER)

        # 3. Poses: [0] parado | [1] passo 1 | [2] passo 2 | [3] pulo
        self.textura_parado_d = quadros_direita[0]
        self.textura_parado_e = quadros_esquerda[0]

        self.passos_direita = [quadros_direita[1], quadros_direita[2]]
        self.passos_esquerda = [quadros_esquerda[1], quadros_esquerda[2]]

        self.textura_pulo_d = quadros_direita[3]
        self.textura_pulo_e = quadros_esquerda[3]

        # 4. Controle de estado e de tempo da animação
        self.quadro_atual: int = 0
        self.tempo_animacao: float = 0.0
        self.virado_para: str = "DIREITA"

    def update(self, delta_time: float = 1 / 60):
        # Impede o jogador de sair pelas laterais (antes dos return abaixo)
        if self.right > LARGURA:
            self.right = LARGURA
        if self.left < 0:
            self.left = 0

        # Lembra para que lado ele está olhando (decide pelo sinal de change_x)
        if self.change_x > 0:
            self.virado_para = "DIREITA"
        elif self.change_x < 0:
            self.virado_para = "ESQUERDA"

        # ESTADO 1 (prioridade máxima): no ar, pulando ou caindo
        if self.change_y != 0:
            if self.virado_para == "DIREITA":
                self.texture = self.textura_pulo_d
            else:
                self.texture = self.textura_pulo_e
            return

        # ESTADO 2: parado no chão
        if self.change_x == 0:
            if self.virado_para == "DIREITA":
                self.texture = self.textura_parado_d
            else:
                self.texture = self.textura_parado_e
            return

        # ESTADO 3: andando no chão (alterna os passos a cada 100 ms)
        self.tempo_animacao += delta_time
        if self.tempo_animacao >= 0.1:
            self.tempo_animacao = 0.0
            self.quadro_atual = (self.quadro_atual + 1) % len(self.passos_direita)

            if self.virado_para == "DIREITA":
                self.texture = self.passos_direita[self.quadro_atual]
            else:
                self.texture = self.passos_esquerda[self.quadro_atual]


class Moeda(arcade.Sprite):
    """Moeda estática: vale 1 ponto e some ao ser coletada."""

    def __init__(self):
        super().__init__("strawberry.png", scale=0.4)
        self.valor = 1


class MoedaEspecial(arcade.Sprite):
    """Moeda dinâmica: vale 5 pontos e rebate nas bordas da tela."""

    def __init__(self):
        super().__init__("cesta_strawberry.png", scale=0.035)
        self.valor = 5

    def update(self, delta_time: float = 1 / 60):
        # Física vetorial: posição += velocidade
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rebote: inverte o vetor (x -1) ao tocar a borda indo para fora
        if (self.left <= 0 and self.change_x < 0) or \
           (self.right >= LARGURA and self.change_x > 0):
            self.change_x *= -1

        if (self.bottom <= 0 and self.change_y < 0) or \
           (self.top >= ALTURA and self.change_y > 0):
            self.change_y *= -1


class Inimigo(arcade.Sprite):
    """
    Inimigo persistente: vaga sozinho pela tela, rebate nas bordas e
    NUNCA é removido ao tocar no jogador.
    """

    def __init__(self):
        super().__init__("strawberry_estragado.png", scale=1)

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if (self.left <= 0 and self.change_x < 0) or \
           (self.right >= LARGURA and self.change_x > 0):
            self.change_x *= -1

        if (self.bottom <= 0 and self.change_y < 0) or \
           (self.top >= ALTURA and self.change_y > 0):
            self.change_y *= -1


class InimigoEspecial(arcade.Sprite):
    """
    Bruxa que persegue o jogador andando no chão (com gravidade, por
    meio de um PhysicsEnginePlatformer próprio) e se teletransporta
    para um ponto aleatório do chão depois de colidir.
    """

    def __init__(self, jogador: Player):
        super().__init__("bruxa_voando.png", scale=0.07)
        self.velocidade = VELOCIDADE_INIMIGO_ESPECIAL
        self.jogador = jogador   # Alvo da perseguição

    def update(self, delta_time: float = 1 / 60):
        # Persegue apenas no eixo X: o eixo Y é da gravidade
        diferenca = self.jogador.center_x - self.center_x
        if abs(diferenca) > self.velocidade:
            if diferenca > 0:
                self.change_x = self.velocidade
            else:
                self.change_x = -self.velocidade
        else:
            self.change_x = 0

        # Mantém dentro das laterais da tela
        if self.left < 0:
            self.left = 0
        if self.right > LARGURA:
            self.right = LARGURA

    def teletransportar(self):
        """Renasce em um X aleatório (longe do jogador), em cima do chão."""
        novo_x = random.randint(60, LARGURA - 60)
        for _ in range(50):
            if abs(novo_x - self.jogador.center_x) > 250:
                break
            novo_x = random.randint(60, LARGURA - 60)

        self.center_x = novo_x
        self.bottom = TOPO_CHAO
        self.change_x = 0
        self.change_y = 0


# ==========================================
# TELA BASE (fundo padronizado)
# ==========================================
class TelaComFundo(arcade.View):
    """View base que desenha o mesmo fundo em todas as telas."""

    def __init__(self):
        super().__init__()

        self.background_list = arcade.SpriteList()

        fundo = arcade.Sprite(ARQUIVO_FUNDO)
        fundo.center_x = LARGURA / 2
        fundo.center_y = ALTURA / 2
        fundo.width = LARGURA
        fundo.height = ALTURA

        self.background_list.append(fundo)

    def desenhar_fundo(self):
        self.background_list.draw()


# ==========================================
# TELA INICIAL
# ==========================================
class TelaInicial(TelaComFundo):
    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        arcade.draw_text("Jogo - Moranguinho", LARGURA / 2, 470,
                         arcade.color.YELLOW, 30, anchor_x="center", bold=True)

        arcade.draw_text("Colete todos os morangos sem ser pego pela bruxa!",
                         LARGURA / 2, 400, arcade.color.WHITE, 16,
                         anchor_x="center")

        opcoes = [
            "[J] Jogar",
            "[I] Instruções",
            "[S] Sobre o Jogo",
            "[R] Ranking",
            "[ESC] Sair",
        ]
        for indice, texto in enumerate(opcoes):
            arcade.draw_text(texto, LARGURA / 2, 330 - indice * 40,
                             arcade.color.YELLOW, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.window.show_view(TelaJogo())
        elif key == arcade.key.I:
            self.window.show_view(TelaInstrucoes())
        elif key == arcade.key.S:
            self.window.show_view(TelaSobre())
        elif key == arcade.key.R:
            self.window.show_view(TelaRanking())
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


# ==========================================
# TELA DE INSTRUÇÕES
# ==========================================
class TelaInstrucoes(TelaComFundo):
    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        arcade.draw_text("INSTRUÇÕES", LARGURA / 2, 520,
                         arcade.color.YELLOW, 26, anchor_x="center", bold=True)

        textos = [
            "OBJETIVO: colete todas as moedas do cenário.",
            "A / D ou setas ← →: andar para a esquerda e para a direita.",
            "W, seta ↑ ou ESPAÇO: pular (não dá para pular duas vezes no ar).",
            "Morango: +1 ponto.   Cesta de morangos: +5 pontos (e ela quica!).",
            "Morango estragado: vaga pela tela, rebate nas bordas e dá -1 ponto.",
            "Bruxa: persegue você pelo chão. Ao encostar, tira -1 ponto",
            "e reaparece em outro lugar do chão.",
            "Escape de todos os inimigos para a pontuação máxima!",
        ]
        for indice, texto in enumerate(textos):
            arcade.draw_text(texto, LARGURA / 2, 455 - indice * 38,
                             arcade.color.WHITE, 15, anchor_x="center")

        arcade.draw_text("Pressione ESC ou M para voltar", LARGURA / 2, 60,
                         arcade.color.LIGHT_RED_OCHRE, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ESCAPE, arcade.key.M):
            self.window.show_view(TelaInicial())


# ==========================================
# TELA SOBRE O JOGO
# ==========================================
class TelaSobre(TelaComFundo):
    def __init__(self):
        super().__init__()

        # Os avatares são sprites guardados em uma SpriteList
        self.sprite_avatares = arcade.SpriteList()
        self.nomes = []   # (nome, posição x) para desenhar embaixo de cada avatar

        quantidade = len(AUTORES)
        for indice, (nome, arquivo) in enumerate(AUTORES):
            # Se a imagem do avatar ainda não existir, usa um morango no lugar
            if not os.path.exists(arquivo):
                arquivo = "strawberry.png"

            x = LARGURA * (indice + 1) / (quantidade + 1)

            avatar = arcade.Sprite(arquivo)
            avatar.scale = 120 / avatar.height   # Altura final de 120 px
            avatar.center_x = x
            avatar.center_y = 270
            self.sprite_avatares.append(avatar)

            self.nomes.append((nome, x))

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        arcade.draw_text("SOBRE O JOGO", LARGURA / 2, 520,
                         arcade.color.YELLOW, 26, anchor_x="center", bold=True)

        arcade.draw_text("Moranguinho: um jogo de plataforma feito com Python Arcade e POO.",
                         LARGURA / 2, 460, arcade.color.WHITE, 15,
                         anchor_x="center")

        arcade.draw_text("Desenvolvido por:", LARGURA / 2, 410,
                         arcade.color.WHITE, 18, anchor_x="center")

        self.sprite_avatares.draw()

        for nome, x in self.nomes:
            arcade.draw_text(nome, x, 170, arcade.color.YELLOW, 18,
                             anchor_x="center", bold=True)

        arcade.draw_text("Pressione ESC ou M para voltar", LARGURA / 2, 60,
                         arcade.color.LIGHT_RED_OCHRE, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ESCAPE, arcade.key.M):
            self.window.show_view(TelaInicial())


# ==========================================
# TELA DO JOGO (PARTIDA)
# ==========================================
class TelaJogo(TelaComFundo):
    def __init__(self):
        super().__init__()

        self.velocidade = VELOCIDADE
        self.pontuacao = 0
        self.tempo_decorrido = 0.0

        # Alerta visual ao levar dano (segundos restantes)
        self.alerta_dano = 0.0
        # Evita tirar vários pontos do inimigo persistente no mesmo toque
        self.tirar_ponto = True

        # Teclas de movimento atualmente seguradas
        self.teclas = set()

        self.sprite_blocos = arcade.SpriteList()
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_inimigo_persistente = arcade.SpriteList()
        self.sprite_inimigo_especial = arcade.SpriteList()
        self.sprite_moedas = arcade.SpriteList()

        self.criar_cenario()
        self.criar_personagens()
        self.criar_moedas()

        # Pontuação máxima = soma do valor de todas as moedas
        self.pontuacao_maxima = 0
        for moeda in self.sprite_moedas:
            self.pontuacao_maxima += moeda.valor

        # Um motor de física para a jogadora...
        self.engine_jogador = arcade.PhysicsEnginePlatformer(
            player_sprite=self.jogador,
            walls=self.sprite_blocos,
            gravity_constant=GRAVIDADE
        )
        # ...e outro para a bruxa, que também anda sobre os blocos
        self.engine_bruxa = arcade.PhysicsEnginePlatformer(
            player_sprite=self.bruxa,
            walls=self.sprite_blocos,
            gravity_constant=GRAVIDADE
        )

    # ---------- construção do cenário ----------
    def criar_cenario(self):
        # Chão: uma fileira de blocos lado a lado na base da tela
        for x in range(TAMANHO_BLOCO // 2, LARGURA + TAMANHO_BLOCO, TAMANHO_BLOCO):
            self.sprite_blocos.append(Bloco(x, TAMANHO_BLOCO / 2))

        # Plataformas suspensas
        for x_inicial, y, quantidade in PLATAFORMAS:
            for i in range(quantidade):
                self.sprite_blocos.append(Bloco(x_inicial + i * TAMANHO_BLOCO, y))

    def criar_personagens(self):
        # Jogadora
        self.jogador = Player()
        self.jogador.center_x = 60
        self.jogador.bottom = TOPO_CHAO
        self.sprite_jogador.append(self.jogador)

        # Inimigo persistente (vaga pela tela inteira)
        self.inimigo_persistente = Inimigo()
        self.inimigo_persistente.center_x = 650
        self.inimigo_persistente.center_y = 500
        self.inimigo_persistente.change_x = self.velocidade
        self.inimigo_persistente.change_y = self.velocidade - 1
        self.sprite_inimigo_persistente.append(self.inimigo_persistente)

        # Inimigo especial (bruxa que persegue pelo chão)
        self.bruxa = InimigoEspecial(self.jogador)
        self.bruxa.center_x = 600
        self.bruxa.bottom = TOPO_CHAO
        self.sprite_inimigo_especial.append(self.bruxa)

    def criar_moedas(self):
        # 25 moedas comuns em posições aleatórias alcançáveis com o pulo
        for _ in range(25):
            moeda = Moeda()
            while True:
                moeda.center_x = random.randint(50, LARGURA - 50)
                moeda.center_y = random.randint(TOPO_CHAO + 40, 330)
                # Sorteia de novo se nasceu dentro de um bloco
                if not arcade.check_for_collision_with_list(moeda, self.sprite_blocos):
                    break
            self.sprite_moedas.append(moeda)

        # 5 moedas especiais, que quicam pela tela
        for _ in range(5):
            moeda = MoedaEspecial()
            moeda.center_x = random.randint(80, LARGURA - 80)
            moeda.center_y = random.randint(150, ALTURA - 80)
            moeda.change_x = random.choice([-1, 1]) * self.velocidade
            moeda.change_y = random.choice([-1, 1]) * (self.velocidade - 1)
            self.sprite_moedas.append(moeda)

    # ---------- desenho ----------
    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        self.sprite_blocos.draw()
        self.sprite_moedas.draw()
        self.sprite_inimigo_persistente.draw()
        self.sprite_inimigo_especial.draw()
        self.sprite_jogador.draw()

        # Alerta visual: clarão vermelho + aviso que some aos poucos
        if self.alerta_dano > 0:
            alpha = int(90 * self.alerta_dano / 0.7)
            arcade.draw_rect_filled(
                arcade.XYWH(LARGURA / 2, ALTURA / 2, LARGURA, ALTURA),
                (255, 0, 0, alpha)
            )
            arcade.draw_text("CUIDADO! -1 PONTO", LARGURA / 2, 530,
                             arcade.color.RED, 22, anchor_x="center", bold=True)

        # HUD
        arcade.draw_text(f"Pontuação: {self.pontuacao}", 10, 570,
                         arcade.color.YELLOW, 14, bold=True)
        arcade.draw_text(f"Tempo: {int(self.tempo_decorrido)}s", LARGURA - 120, 570,
                         arcade.color.YELLOW, 14, bold=True)

    # ---------- lógica ----------
    def dar_dano(self):
        self.pontuacao -= 1
        self.alerta_dano = 0.7

    def on_update(self, delta_time):
        # Cronômetro
        self.tempo_decorrido += delta_time

        # A bruxa decide a direção ANTES de o motor de física movê-la
        self.bruxa.update(delta_time)

        # Motores de física: gravidade, movimento e colisão com os blocos
        self.engine_jogador.update()
        self.engine_bruxa.update()

        # Animação da jogadora, moedas e inimigo persistente
        self.sprite_jogador.update(delta_time)
        self.sprite_moedas.update(delta_time)
        self.sprite_inimigo_persistente.update(delta_time)

        # Coleta de moedas
        moedas_coletadas = arcade.check_for_collision_with_list(
            self.jogador, self.sprite_moedas
        )
        for moeda in moedas_coletadas:
            self.pontuacao += moeda.valor
            moeda.remove_from_sprite_lists()

        # Colisão com o inimigo persistente: NÃO é removido, só tira ponto
        # uma vez por contato (a flag libera de novo quando se afastam)
        colidiu_persistente = arcade.check_for_collision(
            self.jogador, self.inimigo_persistente
        )
        if colidiu_persistente and self.tirar_ponto:
            self.dar_dano()
            self.tirar_ponto = False
        if not colidiu_persistente:
            self.tirar_ponto = True

        # Colisão com a bruxa: tira ponto e ela se teletransporta
        if arcade.check_for_collision(self.jogador, self.bruxa):
            self.dar_dano()
            self.bruxa.teletransportar()

        # Some o alerta aos poucos
        if self.alerta_dano > 0:
            self.alerta_dano -= delta_time

        # Fim de jogo: todas as moedas coletadas
        if len(self.sprite_moedas) == 0:
            self.window.show_view(
                TelaGameOver(
                    self.pontuacao,
                    self.tempo_decorrido,
                    self.pontuacao_maxima
                )
            )

    # ---------- teclado ----------
    def atualizar_direcao(self):
        esquerda = arcade.key.A in self.teclas or arcade.key.LEFT in self.teclas
        direita = arcade.key.D in self.teclas or arcade.key.RIGHT in self.teclas

        if direita and not esquerda:
            self.jogador.change_x = self.velocidade
        elif esquerda and not direita:
            self.jogador.change_x = -self.velocidade
        else:
            self.jogador.change_x = 0

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT):
            self.teclas.add(key)
            self.atualizar_direcao()

        # Pulo: só se estiver apoiada em um bloco (bloqueia pulo duplo)
        elif key in (arcade.key.W, arcade.key.UP, arcade.key.SPACE):
            if self.engine_jogador.can_jump():
                self.jogador.change_y = FORCA_PULO

        # ESC interrompe a partida e volta ao menu
        elif key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT):
            self.teclas.discard(key)
            self.atualizar_direcao()


# ==========================================
# TELA DE GAME OVER (resultado + nome para o ranking)
# ==========================================
class TelaGameOver(TelaComFundo):
    def __init__(self, pontuacao: int, tempo_jogo: float, pontuacao_maxima: int):
        super().__init__()

        self.pontuacao = pontuacao
        self.tempo_jogo = tempo_jogo
        self.pontuacao_maxima = pontuacao_maxima

        # Fase 1 ("nome"): o jogador digita o nome.
        # Fase 2 ("opcoes"): mostra [M], [R] e [ESC].
        self.fase = "nome"
        self.nome_digitado = ""
        self.id_salvo = None      # id do registro criado no banco
        self.erro_banco = False

    def salvar_pontuacao(self, nome: str):
        """Único ponto desta tela que conversa com o banco."""
        return Pontuacao.create(
            nome_jogador=nome,
            pontos=self.pontuacao,
            tempo_partida=self.tempo_jogo
        )

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        perfeito = self.pontuacao == self.pontuacao_maxima

        if perfeito:
            arcade.draw_text("PONTUAÇÃO MÁXIMA! PARABÉNS!", LARGURA / 2, 500,
                             arcade.color.GOLD, 30, anchor_x="center", bold=True)
        else:
            arcade.draw_text("Parabéns! Você terminou o jogo!", LARGURA / 2, 500,
                             arcade.color.YELLOW, 26, anchor_x="center", bold=True)

        arcade.draw_text(f"Pontuação final: {self.pontuacao}", LARGURA / 2, 440,
                         arcade.color.WHITE, 20, anchor_x="center")

        if perfeito:
            arcade.draw_text(f"Tempo total: {self.tempo_jogo:.1f}s", LARGURA / 2, 405,
                             arcade.color.WHITE, 20, anchor_x="center")
            arcade.draw_text("Você escapou de todos os inimigos perfeitamente!",
                             LARGURA / 2, 365, arcade.color.LIGHT_GREEN, 18,
                             anchor_x="center", bold=True)

        if self.fase == "nome":
            arcade.draw_text("Digite seu nome para o ranking:", LARGURA / 2, 300,
                             arcade.color.WHITE, 16, anchor_x="center")
            arcade.draw_rect_outline(
                arcade.XYWH(LARGURA / 2, 250, 360, 50),
                arcade.color.WHITE, border_width=2
            )
            arcade.draw_text(self.nome_digitado + "_", LARGURA / 2, 250,
                             arcade.color.YELLOW, 22, anchor_x="center",
                             anchor_y="center")
            arcade.draw_text("[ENTER] Salvar     [ESC] Pular", LARGURA / 2, 150,
                             arcade.color.LIGHT_RED_OCHRE, 16, anchor_x="center")
        else:
            if self.erro_banco:
                mensagem = "Não foi possível salvar no ranking."
            elif self.id_salvo is not None:
                mensagem = "Pontuação salva no ranking!"
            else:
                mensagem = "Pontuação não salva."
            arcade.draw_text(mensagem, LARGURA / 2, 300,
                             arcade.color.WHITE, 16, anchor_x="center")
            arcade.draw_text("[M] Menu Principal     [R] Ranking     [ESC] Sair do jogo",
                             LARGURA / 2, 200, arcade.color.LIGHT_RED_OCHRE, 18,
                             anchor_x="center")

    def on_text(self, text):
        # Só aceita letras na fase de digitação (isprintable ignora o ENTER)
        if self.fase == "nome":
            if text.isprintable() and len(self.nome_digitado) < LIMITE_NOME:
                self.nome_digitado += text

    def on_key_press(self, key, modifiers):
        if self.fase == "nome":
            if key == arcade.key.BACKSPACE:
                self.nome_digitado = self.nome_digitado[:-1]

            elif key in (arcade.key.ENTER, arcade.key.NUM_ENTER):
                nome = self.nome_digitado.strip()
                if nome:
                    try:
                        registro = self.salvar_pontuacao(nome)
                        self.id_salvo = registro.id
                    except Exception:
                        self.erro_banco = True
                    self.fase = "opcoes"

            elif key == arcade.key.ESCAPE:
                self.fase = "opcoes"   # Pula sem salvar

        else:
            if key == arcade.key.M:
                self.window.show_view(TelaInicial())
            elif key == arcade.key.R:
                self.window.show_view(TelaRanking(destaque_id=self.id_salvo))
            elif key == arcade.key.ESCAPE:
                arcade.close_window()


# ==========================================
# TELA DE RANKING (TOP 10)
# ==========================================
class TelaRanking(TelaComFundo):
    def __init__(self, destaque_id: int = None):
        super().__init__()

        # A consulta roda UMA vez, aqui no __init__ (nunca no on_draw)
        self.melhores = list(
            Pontuacao.select()
            .order_by(Pontuacao.pontos.desc(), Pontuacao.tempo_partida.asc())
            .limit(10)
        )
        # Partida recém-salva para destacar (None quando vem do menu)
        self.destaque_id = destaque_id

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        arcade.draw_text("RANKING - TOP 10", LARGURA / 2, 550,
                         arcade.color.GOLD, 30, anchor_x="center", bold=True)

        # Banco ainda sem pontuações
        if len(self.melhores) == 0:
            arcade.draw_text("Nenhuma pontuação ainda! Seja o primeiro.",
                             LARGURA / 2, 320, arcade.color.WHITE, 20,
                             anchor_x="center")
        else:
            # Cabeçalho das colunas
            y_cab = 500
            arcade.draw_text("POS", 100, y_cab, arcade.color.LIGHT_GRAY, 14, bold=True)
            arcade.draw_text("JOGADOR", 160, y_cab, arcade.color.LIGHT_GRAY, 14, bold=True)
            arcade.draw_text("PONTOS", 450, y_cab, arcade.color.LIGHT_GRAY, 14,
                             bold=True, anchor_x="right")
            arcade.draw_text("TEMPO", 560, y_cab, arcade.color.LIGHT_GRAY, 14,
                             bold=True, anchor_x="right")
            arcade.draw_text("DATA", 700, y_cab, arcade.color.LIGHT_GRAY, 14,
                             bold=True, anchor_x="right")

            # enumerate dá o índice; o Y é proporcional a ele
            for indice, p in enumerate(self.melhores):
                y = 465 - indice * 36

                if p.id == self.destaque_id:
                    cor = arcade.color.YELLOW
                else:
                    cor = arcade.color.WHITE

                arcade.draw_text(f"{indice + 1}º", 100, y, cor, 16)
                arcade.draw_text(p.nome_jogador, 160, y, cor, 16)
                arcade.draw_text(str(p.pontos), 450, y, cor, 16, anchor_x="right")
                arcade.draw_text(f"{p.tempo_partida:.1f}s", 560, y, cor, 16,
                                 anchor_x="right")
                arcade.draw_text(p.data_hora.strftime("%d/%m/%Y"), 700, y, cor, 16,
                                 anchor_x="right")

        arcade.draw_text("[J] Jogar     [ESC] ou [M] Menu", LARGURA / 2, 50,
                         arcade.color.LIGHT_RED_OCHRE, 16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.window.show_view(TelaJogo())
        elif key in (arcade.key.ESCAPE, arcade.key.M):
            self.window.show_view(TelaInicial())


# ==========================================
# FUNÇÃO PRINCIPAL
# ==========================================
def executar():
    # Prepara o banco antes de abrir a janela
    inicializar_banco()

    janela = arcade.Window(LARGURA, ALTURA, NOME)
    janela.show_view(TelaInicial())
    arcade.run()

    # A janela foi fechada: encerra a conexão com o banco
    db.close()


if __name__ == "__main__":
    executar()
