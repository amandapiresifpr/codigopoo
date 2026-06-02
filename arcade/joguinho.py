import arcade
#pip install arcade no terminal
ALTURA = 600
LARGURA = 800
TITULO = "Meu joguinho"


class Jogadora(arcade.Sprite):
     def __init__(self):
          super().__init__("jogadora_right.png", scale = 1)
          # Carregar as texturas para as direções da personagem
          self.texture_right = arcade.load_texture("jogadora_right.png")
          self.texture_left = arcade.load_texture("jogadora_left.png")
 
 # O método update é chamado a cada frame do jogo, e é onde colocamos a lógica
     def update(self, delta_time):
          # Adicionar moviemntação no eixo x e y
          self.center_x += self.change_x
          self.center_y += self.change_y

          # Verificar a direção do movimento para mudar a textura da personagem
          # Se for zero, o personagem mantém a textura atual
          if (self.change_x > 0):
               self.texture = self.texture_right
          elif (self.change_x < 0):
               self.texture = self.texture_left

          # Fazer parar nas bordas da janela
          if (self.right > LARGURA):
               self.change_x = 0

          elif (self.left < 0):
               self.change_x = 0

          if (self.top > ALTURA):
               self.change_y = 0

          elif (self.bottom < 0):
               self.change_y = 0

          

class Strawberry(arcade.Sprite):
     def __init__(self):
          super().__init__("strawberry.png", scale = 0.65)

          
     def update(self, delta_time):
          self.center_x += self.change_x
          self.center_y += self.change_y
          

class JanelaJogo(arcade.Window):
     def __init__(self):
         super().__init__(800, 600, "Meu joguinho")
         arcade.set_background_color((168, 235, 247))
         self.movimento = 0.2

         # Criar minha personagem
         self.jogadora = Jogadora()
         # Posicionar ela na tela
         self.jogadora.center_x = 400
         self.jogadora.center_y = 300
         # Fazer jogadora andar mudando a posição x  e y dela
         self.jogadora.change_x = self.movimento
         self.jogadora.change_y = self.movimento
         # Adicionar a jogadora ao grupo de sprites (append adicionar ao fim da lista)
         self.sprite_jogadora = arcade.SpriteList()
         self.sprite_jogadora.append(self.jogadora)

         # Criar morango
         self.strawberry = Strawberry()
         # Posicionar morango
         self.strawberry.center_x = 500
         self.strawberry.center_y = 275
         # Mudar posição
         self.strawberry.change_x = self.movimento
         self.strawberry.change_y = self.movimento
         # Adicionar o morango ao grupo de sprites (append adicionar ao fim da lista)
         self.sprite_strawberry = arcade.SpriteList()
         self.sprite_strawberry.append(self.strawberry)

     # Desenhar coisas na tela
     def on_draw(self):
         self.clear()
         # Desenhar lista da minha jogadora
         self.sprite_jogadora.draw()
         # Desenhar morango
         self.sprite_strawberry.draw()

     # Atualiza a lógica do jogo e das coisas que estão na tela
     def on_update(self, delta_time):
         # Movimentações e colisões entrarão aqui
         # Atualizar as listas de sprites, o que chama o método update de cada classe
         self.sprite_jogadora.update()
         self.sprite_strawberry.update()
     

def executar():
     jogo = JanelaJogo()
     arcade.run()
    
if __name__ == "__main__":
     executar()
