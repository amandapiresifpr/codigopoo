import arcade, random

class Player(arcade.Sprite):
    def __init__(self):
          # Iniciamos carregando a textura olhando para a direita com 50% do tamanho da imagem
        super().__init__("player_direita.png", scale=0.3)
        
          # Atributos de Estado: Guardamos as duas texturas na memória
        self.textura_direita = self.texture
        self.textura_esquerda = arcade.load_texture("player_esquerda.png")
        
    def update(self):
          # Atributos herdados que atualizam a posição X e Y baseado nas velocidades alteradas pelo teclado
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Lógica de inversão de textura baseada na direção do movimento
        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

class JanelaJogo(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Coletor de Moedas - POO")
        arcade.set_background_color(arcade.color.AMAZON)
        self.setup()

    def setup(self):
        self.jogador = Player() # Cria o objeto para o jogador
        self.jogador.bottom = 0 # Posição inicial x
        self.jogador.left = 0 # Posição inicial y
        self.sprite_jog = arcade.SpriteList() # Lista de sprites para o Jogador
        self.sprite_jog.append(self.jogador) # Adiciona o objeto na lista de sprites
        
        self.velocidade = 10 # Velocidade de movimento 
        self.pontuacao = 0 # Variável para armazenar a pontuação do jogador
        self.cronometro = 0.0 # Cronômetro para o tempo decorrido
        self.jogo_finalizado = False # Flag para saber se o jogo acabou

        # Criar uma lista de moedas
        self.lista_moedas = arcade.SpriteList()
        # Laço para criar 20 instâncias de moedas normais
        for i in range(20):
            # Criar um sprite para cada moeda
            moeda = arcade.Sprite("moeda.png", scale=0.4)
            # Posicionar o sprite da moeda na tela
            moeda.center_x = random.randint(50, 750)
            moeda.center_y = random.randint(50, 550) 
            # Adicionar o sprite da moeda na lista
            self.lista_moedas.append(moeda)

        # Laço para criar 5 moedas especiais
        for i in range(5):
            # Moeda especial é maior e dourada
            moeda_especial = arcade.Sprite("moeda.png", scale=0.6)
            moeda_especial.color = arcade.color.GOLD
            moeda_especial.center_x = random.randint(50, 750)
            moeda_especial.center_y = random.randint(50, 550)
            self.lista_moedas.append(moeda_especial)

    def on_draw(self):
        self.clear()
        self.lista_moedas.draw()
        self.sprite_jog.draw()
        # Desenha o texto de pontuação na tela
        arcade.draw_text(f"Moedas Coletadas: {self.pontuacao}", 10, 570, arcade.color.WHITE, 14)
        # Desenha o cronômetro na tela
        arcade.draw_text(f"Tempo: {self.cronometro:.2f}s", 10, 545, arcade.color.WHITE, 14)

        if self.jogo_finalizado:
            # Mensagem de vitória
            arcade.draw_text("ARRASOU DIVA!", 300, 350, arcade.color.YELLOW, 30, bold=True)
            arcade.draw_text("Você coletou todas as moedas!", 200, 300, arcade.color.WHITE, 20)
            arcade.draw_text(f"Tempo Final: {self.cronometro:.2f}s", 310, 260, arcade.color.GOLD, 18)
            arcade.draw_text("Pressione R para recomeçar ou ESC para sair", 180, 200, arcade.color.WHITE, 16)


    def on_update(self, delta_time):
        if not self.jogo_finalizado:
            self.jogador.update()
            self.cronometro += delta_time

            # VERIFICAÇÃO DE COLISÃO:
            # Retorna uma lista com todas as moedas que colidiram com o jogador
            moedas_colididas = arcade.check_for_collision_with_list(self.jogador, self.lista_moedas)
            # Tratamento dos objetos atingidos
            for moeda in moedas_colididas:
                # Destrói o objeto moeda, retirando-o do jogo
                moeda.remove_from_sprite_lists()
                # Incrementa a pontuação do jogador
                self.pontuacao += 1
            
            # Verifica se todas as moedas foram coletadas
            if len(self.lista_moedas) == 0:
                self.jogo_finalizado = True

    # Gerenciamento do Teclado (Explicado abaixo)
    def on_key_press(self, key, modifiers):
        if key == arcade.key.R: # Tecla R para recomeçar o jogo
            self.setup()
            
        if key == arcade.key.LEFT or key == arcade.key.A: # Seta da esquerda ou A
            self.jogador.change_x = -self.velocidade
        elif key == arcade.key.RIGHT or key == arcade.key.D: # Seta da direita ou D
            self.jogador.change_x = self.velocidade
        elif key == arcade.key.UP or key == arcade.key.W: # Seta de cima ou W
            self.jogador.change_y = self.velocidade
        elif key == arcade.key.DOWN or key == arcade.key.S: # Seta de baixo ou s
            self.jogador.change_y = -self.velocidade

        if key == arcade.key.ESCAPE: # Tecla ESC para fechar o jogo
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        # Ao soltar uma tecla, verifica se é do eixo X ou Y para zerar a velocidade
        if key in [arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D]:
            self.jogador.change_x = 0
        if key in [arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S]:
            self.jogador.change_y = 0


def main():
    janela = JanelaJogo()
    arcade.run()

if __name__ == "__main__":    
    main()