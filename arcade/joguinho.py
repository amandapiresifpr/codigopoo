import arcade
import random
#pip install arcade no terminal
ALTURA = 600
LARGURA = 800
TITULO = "Meu joguinho"


class Jogadora(arcade.Sprite):
     def __init__(self):
          super().__init__("jogadora_right.png", scale = 1.3)
          # Carregar as texturas para as direções da personagem
          self.texture_right = arcade.load_texture("jogadora_right.png")
          self.texture_left = arcade.load_texture("jogadora_left.png")
 
     # O método update é chamado a cada frame do jogo, e é onde colocamos a lógica
     def update(self, delta_time):
          pass
           
          # Adicionar movimentação no eixo x e y
          self.center_x += self.change_x
          self.center_y += self.change_y

          
          # Verificar a direção do movimento para mudar a textura da personagem
          # Se for zero, o personagem mantém a textura atual
          if (self.change_x > 0):
               self.texture = self.texture_right
          elif (self.change_x < 0):
               self.texture = self.texture_left

          # Manter o player dentro da janela
          # Limita ele na borda da direita
          if self.right > LARGURA:
               self.change_x = 0
               self.right = LARGURA
                    
          # Limita ele na borda da esquerda
          if self.left < 0:
               self.change_x = 0
               self.left = 0
          
          # Limita ele na borda superior
          if self.top > ALTURA:
               self.change_y = 0
               self.top = ALTURA

          # Limita ele na borda inferior
          if self.bottom < 0:
               self.change_y = 0
               self.bottom = 0



class Strawberry(arcade.Sprite):
     def __init__(self):
          super().__init__("strawberry.png", scale = 0.8)

          
     def update(self, delta_time):
          self.center_x += self.change_x
          self.center_y += self.change_y
          
           # Fazer parar nas bordas da janela
          if (self.right > LARGURA or self.left < 0):
               self.change_x *= -1

          if (self.top > ALTURA or self.bottom < 0):
               self.change_y  *= -1


class JanelaJogo(arcade.Window):
     def __init__(self):
         super().__init__(800, 600, "Meu joguinho")
         arcade.set_background_color((168, 235, 247))
         self.velocidade = 3

         # Criar minha personagem
         self.jogadora = Jogadora()
         # Posicionar ela na tela
         self.jogadora.center_x = 400
         self.jogadora.center_y = 300
         # Fazer jogadora andar mudando a posição x  e y dela
         self.jogadora.change_x = self.velocidade
         self.jogadora.change_y = self.velocidade
         # Adicionar a jogadora ao grupo de sprites (append adicionar ao fim da lista)
         self.sprite_jogadora = arcade.SpriteList()
         self.sprite_jogadora.append(self.jogadora)

         # Criar morango
         self.strawberry = Strawberry()
         # Posicionar morango
         self.strawberry.center_x = 500
         self.strawberry.center_y = 275
         # Mudar posição
         self.strawberry.change_x = self.velocidade
         self.strawberry.change_y = self.velocidade
         # Adicionar o morango ao grupo de sprites (append adicionar ao fim da lista)
         self.sprite_strawberry = arcade.SpriteList()
         self.sprite_strawberry.append(self.strawberry)

         # laço de repetição 
         for i in range(20):
              self.strawberry_simples = Strawberry()

              self.strawberry_simples.center_x = random.randint(50, LARGURA - 50)
              self.strawberry_simples.center_y = random.randint(50, ALTURA-50)

              velocidade = random.randint(1,10)
              if(velocidade < 3):
                   self.strawberry_simples.change_x = velocidade
                   self.strawberry_simples.change_y = velocidade

              self.sprite_strawberry.append(self.strawberry_simples)
              
         

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

     def on_key_press(self, key, modifiers):
          if (key == arcade.key.RIGHT): # Seta da esquerda (A)
               self.jogadora.change_x += self.velocidade
          elif (key == arcade.key.LEFT):
               self.jogadora.change_x -= self.velocidade
          elif (key == arcade.key.UP):
               self.jogadora.change_y += self.velocidade
          elif (key == arcade.key.DOWN):
               self.jogadora.change_y -= self.velocidade

          # Fechar janela
          if(key == arcade.key.ESCAPE):
               arcade.close_window()
          
     def on_key_release(self, key, modifiers):
          if (key == arcade.key.RIGHT or key == arcade.key.LEFT):
               self.jogadora.change_x = 0

          elif (key == arcade.key.UP or key == arcade.key.DOWN):
               self.jogadora.change_y = 0 

def executar():
     jogo = JanelaJogo()
     arcade.run()
    
if __name__ == "__main__":
     executar()
