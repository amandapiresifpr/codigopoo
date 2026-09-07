import arcade
import random

# Constantes globais
ALTURA = 600
LARGURA = 800
NOME = "Moranguinho"

VELOCIDADE = 4
VELOCIDADE_INIMIGO_ESPECIAL = 1.2
ARQUIVO_FUNDO = "fundo.png"


class TelaComFundo(arcade.View):
    """View base que desenha o fundo padronizado em todas as telas."""

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


class Player(arcade.Sprite):
    """Jogador com movimento livre, sem gravidade."""

    def __init__(self):
        super().__init__("jogadora_right.png", scale=1)

        self.textura_direita = self.texture
        self.textura_esquerda = arcade.load_texture("jogadora_left.png")

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Troca a textura de acordo com a direção horizontal.
        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        # Impede o jogador de sair da tela.
        if self.right > LARGURA:
            self.right = LARGURA
            self.change_x = 0

        if self.left < 0:
            self.left = 0
            self.change_x = 0

        if self.top > ALTURA:
            self.top = ALTURA
            self.change_y = 0

        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0


class Inimigo(arcade.Sprite):
    """Inimigo persistente que se movimenta sozinho e rebate nas bordas."""

    def __init__(self):
        super().__init__("strawberry_estragado.png", scale=1)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Inverte a velocidade ao tocar nas bordas.
        if self.left <= 0 or self.right >= LARGURA:
            self.change_x *= -1

        if self.bottom <= 0 or self.top >= ALTURA:
            self.change_y *= -1


class InimigoEspecial(arcade.Sprite):
    """Bruxa que segue o jogador e se teleporta após uma colisão."""

    def __init__(self):
        super().__init__("bruxa_voando.png", scale=0.07)

        self.velocidade = VELOCIDADE_INIMIGO_ESPECIAL
        self.jogador = None

    def update(self, delta_time):
        if self.jogador is not None:
            # Segue o jogador no eixo X.
            if self.jogador.center_x > self.center_x:
                self.change_x = self.velocidade
            elif self.jogador.center_x < self.center_x:
                self.change_x = -self.velocidade
            else:
                self.change_x = 0

            # Segue o jogador no eixo Y.
            if self.jogador.center_y > self.center_y:
                self.change_y = self.velocidade
            elif self.jogador.center_y < self.center_y:
                self.change_y = -self.velocidade
            else:
                self.change_y = 0

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Mantém a bruxa dentro da tela.
        if self.left < 0:
            self.left = 0
        elif self.right > LARGURA:
            self.right = LARGURA

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > ALTURA:
            self.top = ALTURA


class Moeda(arcade.Sprite):
    """Moeda comum: vale 1 ponto."""

    def __init__(self):
        super().__init__("strawberry.png", scale=0.4)
        self.valor = 1


class MoedaEspecial(arcade.Sprite):
    """Moeda especial: vale 5 pontos e se movimenta."""

    def __init__(self):
        super().__init__("cesta_strawberry.png", scale=0.035)
        self.valor = 5

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rebater nas bordas invertendo o vetor de velocidade.
        if self.left <= 0 or self.right >= LARGURA:
            self.change_x *= -1

        if self.bottom <= 0 or self.top >= ALTURA:
            self.change_y *= -1


class TelaInicial(TelaComFundo):
    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        arcade.draw_text(
            "Jogo - Moranguinho",
            LARGURA / 2,
            470,
            arcade.color.YELLOW,
            25,
            anchor_x="center"
        )

        arcade.draw_text(
            "OBJETIVO",
            LARGURA / 2,
            400,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "Colete todas as morangos (não estragados) sem ser pego pela bruxa.",
            LARGURA / 2,
            365,
            arcade.color.YELLOW_GREEN,
            16,
            anchor_x="center"
        )

        arcade.draw_text(
            "Morango: +1 ponto     Cesta de morangos: +5 pontos",
            LARGURA / 2,
            335,
            arcade.color.WHITE,
            16,
            anchor_x="center"
        )

        arcade.draw_text(
            "[I] Instruções     [S] Sobre     [J] Jogar     [ESC] Sair",
            LARGURA / 2,
            100,
            arcade.color.YELLOW,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.window.show_view(TelaJogo())
        elif key == arcade.key.I:
            self.window.show_view(TelaInstrucoes())
        elif key == arcade.key.S:
            self.window.show_view(TelaSobre())
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


class TelaInstrucoes(TelaComFundo):
    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        arcade.draw_text(
            "INSTRUÇÕES",
            LARGURA / 2,
            470,
            arcade.color.YELLOW,
            26,
            anchor_x="center"
        )

        textos = [
            "W ou S: mover para cima ou para baixo",
            "A ou D: mover para a esquerda ou para a direita",
            "Setas também podem ser usadas para movimentação.",
            "Morango: +1 ponto.",
            "Cesta de morangos: +5 pontos.",
            "Os inimigos tiram 1 ponto por colisão.",
            "A bruxa persegue o jogador e muda de posição após a colisão."
        ]

        for indice, texto in enumerate(textos):
            arcade.draw_text(
                texto,
                LARGURA / 2,
                390 - indice * 38,
                arcade.color.WHITE,
                15,
                anchor_x="center"
            )

        arcade.draw_text(
            "Pressione ESC ou M para voltar",
            LARGURA / 2,
            70,
            arcade.color.LIGHT_RED_OCHRE,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ESCAPE, arcade.key.M):
            self.window.show_view(TelaInicial())


class TelaSobre(TelaComFundo):
    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        arcade.draw_text(
            "SOBRE O JOGO",
            LARGURA / 2,
            470,
            arcade.color.YELLOW,
            26,
            anchor_x="center"
        )

        arcade.draw_text(
            "Moranguinho",
            LARGURA / 2,
            380,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            "Um jogo de coleta e desvio criado com Python e Arcade, " \
            "por Amanda.",
            LARGURA / 2,
            335,
            arcade.color.WHITE,
            16,
            anchor_x="center"
        )

        arcade.draw_text(
            "Colete todas os morangos (aptos para alimentção) e fuja da bruxa!",
            LARGURA / 2,
            295,
            arcade.color.WHITE,
            16,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione ESC ou M para voltar",
            LARGURA / 2,
            90,
            arcade.color.LIGHT_RED_OCHRE,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ESCAPE, arcade.key.M):
            self.window.show_view(TelaInicial())


class TelaJogo(TelaComFundo):
    def __init__(self):
        super().__init__()

        self.velocidade = VELOCIDADE
        self.pontuacao = 0
        self.tempo_decorrido = 0.0

        # Permite tirar apenas 1 ponto enquanto o jogador permanece
        # encostado em um inimigo.
        self.tirar_ponto = True
        self.alerta_dano = 0

        # Criar jogador.
        self.jogador = Player()
        self.jogador.center_x = 50
        self.jogador.center_y = 50

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

        # Criar inimigo persistente.
        self.inimigo_persistente = Inimigo()
        self.inimigo_persistente.center_x = 650
        self.inimigo_persistente.center_y = 500
        self.inimigo_persistente.change_x = self.velocidade
        self.inimigo_persistente.change_y = self.velocidade - 1

        self.sprite_inimigo_persistente = arcade.SpriteList()
        self.sprite_inimigo_persistente.append(self.inimigo_persistente)

        # Criar inimigo especial.
        self.inimigo_especial = InimigoEspecial()
        self.inimigo_especial.center_x = 350
        self.inimigo_especial.center_y = 300
        self.inimigo_especial.jogador = self.jogador
        self.inimigo_especial.change_x = 0
        self.inimigo_especial.change_y = 0

        self.sprite_inimigo_especial = arcade.SpriteList()
        self.sprite_inimigo_especial.append(self.inimigo_especial)

        # Lista geral de moedas.
        self.sprite_moedas = arcade.SpriteList()

        # Pelo menos 25 moedas comuns.
        for _ in range(25):
            moeda = Moeda()
            moeda.center_x = random.randint(50, LARGURA - 50)
            moeda.center_y = random.randint(50, ALTURA - 50)
            self.sprite_moedas.append(moeda)

        # Moedas especiais.
        self.moedas_especiais = arcade.SpriteList()

        for _ in range(5):
            moeda = MoedaEspecial()
            moeda.center_x = random.randint(80, LARGURA - 80)
            moeda.center_y = random.randint(80, ALTURA - 80)

            moeda.change_x = random.choice([-1, 1]) * self.velocidade
            moeda.change_y = random.choice([-1, 1]) * (self.velocidade - 1)

            self.moedas_especiais.append(moeda)
            self.sprite_moedas.append(moeda)

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        # Objetos do jogo.
        self.sprite_moedas.draw()
        self.sprite_inimigo_persistente.draw()
        self.sprite_inimigo_especial.draw()
        self.sprite_jogador.draw()

        # HUD.
        arcade.draw_text(
            f"Pontuação: {self.pontuacao}",
            10,
            570,
            arcade.color.YELLOW,
            14
        )

        arcade.draw_text(
            f"Tempo: {int(self.tempo_decorrido)}s",
            LARGURA - 120,
            570,
            arcade.color.YELLOW,
            14
        )

        if self.alerta_dano > 0:
            arcade.draw_text(
                "CUIDADO! -1 PONTO",
                LARGURA / 2,
                530,
                arcade.color.RED,
                18,
                anchor_x="center"
            )

    def on_update(self, delta_time):
        self.tempo_decorrido += delta_time

        # Atualizar todos os elementos.
        self.sprite_moedas.update()
        self.sprite_jogador.update()
        self.sprite_inimigo_persistente.update()
        self.sprite_inimigo_especial.update()

        # Coleta das moedas.
        moedas_coletadas = arcade.check_for_collision_with_list(
            self.jogador,
            self.sprite_moedas
        )

        for moeda in moedas_coletadas:
            self.pontuacao += moeda.valor
            moeda.remove_from_sprite_lists()

        # Colisão com inimigo persistente.
        colisao_persistente = arcade.check_for_collision_with_list(
            self.jogador,
            self.sprite_inimigo_persistente
        )

        # Colisão com inimigo especial.
        colisao_especial = arcade.check_for_collision_with_list(
            self.jogador,
            self.sprite_inimigo_especial
        )

        if (colisao_persistente or colisao_especial) and self.tirar_ponto:
            self.pontuacao -= 1
            self.alerta_dano = 0.7
            self.tirar_ponto = False

            # A bruxa teleporta depois da colisão.
            if colisao_especial:
                self.inimigo_especial.center_x = random.randint(
                    60, LARGURA - 60
                )
                self.inimigo_especial.center_y = random.randint(
                    60, ALTURA - 60
                )

        # Quando o jogador deixa de encostar, pode perder ponto novamente
        # em uma próxima colisão.
        if not colisao_persistente and not colisao_especial:
            self.tirar_ponto = True

        if self.alerta_dano > 0:
            self.alerta_dano -= delta_time

        # Vitória quando todas as moedas forem coletadas.
        if len(self.sprite_moedas) == 0:
            self.window.show_view(
                TelaVitoria(
                    self.pontuacao,
                    int(self.tempo_decorrido)
                )
            )

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.LEFT):
            self.jogador.change_x = -self.velocidade

        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.jogador.change_x = self.velocidade

        elif key in (arcade.key.W, arcade.key.UP):
            self.jogador.change_y = self.velocidade

        elif key in (arcade.key.S, arcade.key.DOWN):
            self.jogador.change_y = -self.velocidade

        elif key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())

    def on_key_release(self, key, modifiers):
        if key in (
            arcade.key.A,
            arcade.key.D,
            arcade.key.LEFT,
            arcade.key.RIGHT
        ):
            self.jogador.change_x = 0

        if key in (
            arcade.key.W,
            arcade.key.S,
            arcade.key.UP,
            arcade.key.DOWN
        ):
            self.jogador.change_y = 0


class TelaVitoria(TelaComFundo):
    def __init__(self, pontuacao_final, tempo_final):
        super().__init__()

        self.pontuacao = pontuacao_final
        self.cronometro = tempo_final

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        arcade.draw_text(
            "Fim do Jogo!",
            LARGURA / 2,
            400,
            arcade.color.YELLOW,
            24,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Sua pontuação foi: {self.pontuacao}",
            LARGURA / 2,
            350,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Tempo: {self.cronometro}s",
            LARGURA / 2,
            315,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "[J] Jogar novamente     [ESC] Voltar ao menu",
            LARGURA / 2,
            220,
            arcade.color.LIGHT_RED_OCHRE,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.window.show_view(TelaJogo())

        elif key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())


def executar():
    janela = arcade.Window(LARGURA, ALTURA, NOME)
    janela.show_view(TelaInicial())
    arcade.run()


if __name__ == "__main__":
    executar()
