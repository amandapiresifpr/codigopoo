import arcade
#pip install arcade no terminal
ALTURA = 600
LARGURA = 800
TITULO = "Meu joguinho"

class Jogadora(arcade.Sprite):
     def __init__(self):
          super().__init__("jogadora_right.png", scale = 0.04)
          self.textura_direita = arcade.load_texture("jogadora_right.png")
          self.textura_esquerda = arcade.load_texture("jogadora_left.png")
 
     def update(self, delta_time):
          pass

class JanelaJogo(arcade.Window):
     def __init__(self):
         super().__init__(800, 600, "Meu joguinho")
         arcade.set_background_color((168, 235, 247))

         #Criar minha personagem
         self.jogadora = Jogadora()
         #Posicionar ela na tela
         self.jogadora.center_x = 400
         self.jogadora.center_y = 300

     #Desenhar coisas na tela
     def on_draw(self):
         self.clear()
         #Desenhar minha jogadora
         arcade.draw_sprite(self.jogadora)

     def on_update(self, delta_time):
         pass
     
def executar():
     jogo = JanelaJogo()
     arcade.run()
    
if __name__ == "__main__":
     executar()
