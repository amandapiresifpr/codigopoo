
import arcade
import random

LARGURA = 800
ALTURA = 600
TITULO = "Coletor de Tesouros"


class Jogadora(arcade.Sprite):

    def __init__(self):
        super().__init__("jogadora_right.png", scale=1.3)

        self.texture_right = arcade.load_texture("jogadora_right.png")
        self.texture_left = arcade.load_texture("jogadora_left.png")

    def update(self, delta_time=1 / 60):

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x > 0:
            self.texture = self.texture_right

        elif self.change_x < 0:
            self.texture = self.texture_left

        if self.right > LARGURA:
            self.right = LARGURA

        if self.left < 0:
            self.left = 0

        if self.top > ALTURA:
            self.top = ALTURA

        if self.bottom < 0:
            self.bottom = 0


class Moeda(arcade.Sprite):

    def __init__(self):
        super().__init__("strawberry.png", scale=0.8)


class MoedaEspecial(arcade.Sprite):

    def __init__(self):
        super().__init__("cesta_strawberry.png", scale=0.8)

    def update(self, delta_time=1 / 60):

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > LARGURA or self.left < 0:
            self.change_x *= -1

        if self.top > ALTURA or self.bottom < 0:
            self.change_y *= -1


class Inimigo(arcade.Sprite):

    def __init__(self):
        super().__init__("bruxa.png", scale=0.08)

    def update(self, delta_time=1 / 60):

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > LARGURA or self.left < 0:
            self.change_x *= -1

        if self.top > ALTURA or self.bottom < 0:
            self.change_y *= -1


class InimigoEspecial(arcade.Sprite):

    def __init__(self):
        super().__init__("bruxa_voando.png", scale=0.08)

    def update(self, delta_time=1 / 60):

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > LARGURA or self.left < 0:
            self.change_x *= -1

        if self.top > ALTURA or self.bottom < 0:
            self.change_y *= -1


class JanelaJogo(arcade.Window):

    def __init__(self):

        super().__init__(LARGURA, ALTURA, TITULO)

        arcade.set_background_color((168, 235, 247))

        self.velocidade = 5
        self.pontos = 0

        self.alerta = ""
        self.tempo_alerta = 0

        self.fim_jogo = False

        # Jogadora

        self.jogadora = Jogadora()
        self.jogadora.center_x = 400
        self.jogadora.center_y = 300

        self.sprite_jogadora = arcade.SpriteList()
        self.sprite_jogadora.append(self.jogadora)

        # Moedas

        self.sprite_moedas = arcade.SpriteList()

        for i in range(25):

            moeda = Moeda()

            moeda.center_x = random.randint(50, 750)
            moeda.center_y = random.randint(50, 550)

            self.sprite_moedas.append(moeda)

        # Moeda Especial

        self.moeda_especial = MoedaEspecial()

        self.moeda_especial.center_x = 500
        self.moeda_especial.center_y = 300

        self.moeda_especial.change_x = 4
        self.moeda_especial.change_y = 4

        self.sprite_moedas.append(self.moeda_especial)

        # Inimigo

        self.sprite_inimigos = arcade.SpriteList()

        self.inimigo = Inimigo()

        self.inimigo.center_x = 150
        self.inimigo.center_y = 150

        self.inimigo.change_x = 3
        self.inimigo.change_y = 3

        self.sprite_inimigos.append(self.inimigo)

        # Inimigo Especial

        self.inimigo_especial = InimigoEspecial()

        self.inimigo_especial.center_x = 650
        self.inimigo_especial.center_y = 450

        self.inimigo_especial.change_x = 5
        self.inimigo_especial.change_y = 5

        self.sprite_inimigos.append(self.inimigo_especial)

    def on_draw(self):

        self.clear()

        self.sprite_jogadora.draw()
        self.sprite_moedas.draw()
        self.sprite_inimigos.draw()

        arcade.draw_text(
            f"Pontos: {self.pontos}",
            10,
            560,
            arcade.color.BLACK,
            20
        )

        if self.tempo_alerta > 0:

            arcade.draw_text(
                self.alerta,
                220,
                560,
                arcade.color.RED,
                20
            )

        if self.fim_jogo:

            arcade.draw_text(
                "VOCE VENCEU!",
                250,
                300,
                arcade.color.GREEN,
                40
            )

    def on_update(self, delta_time):

        if self.fim_jogo:
            return

        self.sprite_jogadora.update()
        self.sprite_moedas.update()
        self.sprite_inimigos.update()

        # Colisão moedas

        colisoes = arcade.check_for_collision_with_list(
            self.jogadora,
            self.sprite_moedas
        )

        for moeda in colisoes:

            if isinstance(moeda, MoedaEspecial):
                self.pontos += 5
            else:
                self.pontos += 1

            moeda.remove_from_sprite_lists()

        # Inimigo normal

        if arcade.check_for_collision(
            self.jogadora,
            self.inimigo
        ):

            self.pontos -= 1

            self.alerta = "Cuidado! Bruxa te acertou!"
            self.tempo_alerta = 60

        # Inimigo especial

        if arcade.check_for_collision(
            self.jogadora,
            self.inimigo_especial
        ):

            self.pontos -= 1

            self.inimigo_especial.center_x = random.randint(50, 750)
            self.inimigo_especial.center_y = random.randint(50, 550)

            self.alerta = "Bruxa voadora apareceu!"
            self.tempo_alerta = 60

        if self.tempo_alerta > 0:
            self.tempo_alerta -= 1

        moedas_restantes = 0

        for sprite in self.sprite_moedas:
            if isinstance(sprite, Moeda):
                moedas_restantes += 1

        if moedas_restantes == 0:
            self.fim_jogo = True

    def on_key_press(self, key, modifiers):

        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.jogadora.change_x = self.velocidade

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.jogadora.change_x = -self.velocidade

        elif key == arcade.key.UP or key == arcade.key.W:
            self.jogadora.change_y = self.velocidade

        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.jogadora.change_y = -self.velocidade

        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):

        if key in (
            arcade.key.RIGHT,
            arcade.key.LEFT,
            arcade.key.D,
            arcade.key.A
        ):
            self.jogadora.change_x = 0

        if key in (
            arcade.key.UP,
            arcade.key.DOWN,
            arcade.key.W,
            arcade.key.S
        ):
            self.jogadora.change_y = 0


def executar():

    JanelaJogo()
    arcade.run()


if __name__ == "__main__":
    executar()

