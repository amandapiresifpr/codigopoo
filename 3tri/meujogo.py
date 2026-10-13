import math
import os
import random

import arcade

# Tudo o que é banco de dados mora em banco.py
from banco import db, Pontuacao, inicializar_banco

# Texto em pixel art (vermelho e amarelo), igual ao dos títulos em PNG
from texto_pixel import (texto_pixelado, PALETA_TITULO, PALETA_MENU,
                         PALETA_OURO, PALETA_TEXTO, PALETA_VERDE)

# ==========================================
# CONSTANTES GLOBAIS
# ==========================================
ALTURA = 600
LARGURA = 800
NOME = "Moranguinho"

VELOCIDADE = 4                      # Velocidade horizontal do jogador
VELOCIDADE_INIMIGO_ESPECIAL = 1.2   # Velocidade da bruxa voadora
GRAVIDADE = 0.5                     # gravity_constant do motor de física

# Pulo: o pulo DUPLO (no ar) é o pulo "completo" de antes. O pulo normal
# (do chão) tem 75% dessa altura. A altura de um pulo cresce com o
# QUADRADO da velocidade inicial (h = v² / 2g), por isso a força do pulo
# normal é FORCA_PULO * raiz(0.75), e não FORCA_PULO * 0.75.
FORCA_PULO = 16                     # change_y do pulo duplo
FATOR_PULO_NORMAL = 0.75            # altura do pulo normal / altura do duplo
FORCA_PULO_NORMAL = FORCA_PULO * math.sqrt(FATOR_PULO_NORMAL)
PULO_DUPLO = True                   # False volta a bloquear o pulo duplo

VIDAS = 5                           # Vidas no início da partida

TAMANHO_BLOCO = 75                  # bloco.png tem 75x75 px
# Y (contado a partir da base da janela) onde começa a grama do chão
# desenhado no fundo.png. Meça com:  python medir_chao.py
TOPO_CHAO = 131

ESCALA_PLAYER = 0.75                # Quadros da jogadora têm 100x110 px (cerca de 78 px de altura na tela)
LIMITE_NOME = 12                    # Máximo de letras no nome do ranking

ARQUIVO_FUNDO = "fundo.png"
ARQUIVO_SPRITESHEET = "player_direita.png"
ARQUIVO_EXPLOSAO = "explosao.png"   # 6 quadros de 128x128 px, em uma linha
ARQUIVO_CORACAO_CHEIO = "coracao_cheio.png"   # 42x39 px
ARQUIVO_CORACAO_VAZIO = "coracao_vazio.png"   # 42x39 px
ARQUIVO_VENENO = "veneno.png"       # 6 quadros de 128x128 px, em uma linha

# Textos pixelados (vermelho e amarelo), gerados por gerar_titulos.py
ARQUIVO_BRUXA = "bruxa_sheet.png"   # 4 quadros de 280x270 px, em uma linha (1120x270)
ESCALA_BRUXA = 0.38                 # tamanho da bruxa na tela (cerca de 95 x 100 px)
BALANCO_BRUXA = 0.5                 # quanto ela balança de um lado pro outro
TEMPO_QUADRO_BRUXA = 0.2            # segundos que cada quadro da bruxa fica na tela
# Ordem dos quadros em "vai e volta" (0,1,2,3,2,1): o quadro 3 nunca pula
# direto para o 0, que é a troca mais brusca do desenho.
ORDEM_VOO_BRUXA = [0, 1, 2, 3, 2, 1]
ARQUIVO_TITULO = "titulo.png"       # MORANGUINHO + subtítulo
ARQUIVOS_MENU = [                   # opções do menu, de cima para baixo
    "menu_jogar.png",
    "menu_instrucoes.png",
    "menu_sobre.png",
    "menu_ranking.png",
    "menu_sair.png",
]
ARQUIVO_FIM_DERROTA = "fim_derrota.png"
ARQUIVO_FIM_VITORIA = "fim_vitoria.png"
ARQUIVO_FIM_PERFEITO = "fim_perfeito.png"

# Efeitos visuais da colisão (duração em segundos)
TEMPO_INVENCIVEL = 1.5      # Imunidade depois de levar um golpe
TEMPO_FLASH = 0.3           # Clarão vermelho
TEMPO_TREMOR = 0.35         # Tremor de tela
INTENSIDADE_TREMOR = 8      # Deslocamento máximo da câmera, em pixels

# Veneno do morango estragado
TEMPO_VENENO = 3.0              # Quanto tempo a jogadora fica envenenada
TEMPO_PARALISIA = 2.0           # Quanto tempo ela fica paralisada (s)
COR_VENENO = (120, 255, 100)    # Cor (R, G, B) que "tinge" a jogadora
ESCALA_NUVEM_VENENO = 1.25      # Tamanho da animação de veneno
COR_FLASH_VENENO = (0, 255, 0)  # Clarão VERDE (golpe do morango estragado)
COR_FLASH_BRUXA = (255, 0, 0)   # Clarão VERMELHO (golpe da bruxa)

# Morango que a jogadora perde ao ser envenenada
DURACAO_VOO_MORANGO = 0.6       # Tempo que ele leva voando até o destino (s)
ALTURA_ARCO_MORANGO = 90        # Altura do arco do voo, em pixels

# Distribuição das moedas: para cada moeda sorteamos vários candidatos e
# ficamos com o que está MAIS LONGE das moedas que já existem.
CANDIDATOS_MORANGO = 40         # Quantos pontos sorteados por moeda
MARGEM_MORANGO = 40             # Distância mínima das laterais da tela
ALTURA_MAX_MORANGO = 450        # Altura máxima onde uma moeda pode nascer

# Plataformas suspensas: (x do primeiro bloco, y do centro, quantidade de blocos)
# Alturas dos degraus: 256, 366 e 476 (eram 200, 310 e 420 quando o chão ficava
# em 75; subiram 56 px junto com o TOPO_CHAO). A diferença entre degraus
# (110 px) cabe no pulo normal (cerca de 185 px), e o espaço entre o chão e a
# primeira plataforma (87 px) deixa a jogadora passar por baixo.
PLATAFORMAS = [
    (40, 256, 2),
    (575, 256, 3),
    (260, 366, 2),
    (450, 476, 2),
]

# Integrantes do grupo: (nome, arquivo do avatar).
# Se o arquivo do avatar não existir na pasta, a tela Sobre mostra um morango.
AUTORES = [
    ("Amanda Pires", "avatar_amanda.png"),
]


def sprite_texto(texto: str, tamanho: int, escala: int, paleta: list,
                 x: float, y: float) -> arcade.Sprite:
    """
    Cria um sprite com o texto em pixel art (a imagem é gerada na hora
    pelo texto_pixel.py). Usado nas telas de Instruções, Sobre e Ranking.
    """
    imagem = texto_pixelado(texto, tamanho, escala, paleta)
    sprite = arcade.Sprite(arcade.Texture(imagem))
    sprite.center_x = x
    sprite.center_y = y
    return sprite


# Cache das texturas de texto: um mesmo texto (com o mesmo tamanho e cores)
# é gerado UMA vez e reaproveitado. Sem isso, o texto que muda (pontuação,
# tempo, contagem do veneno) geraria uma imagem do Pillow a cada mudança.
CACHE_TEXTURAS_TEXTO = {}


def textura_pixel(texto: str, tamanho: int, escala: int, paleta: list):
    chave = (texto, tamanho, escala, id(paleta))
    if chave not in CACHE_TEXTURAS_TEXTO:
        imagem = texto_pixelado(texto, tamanho, escala, paleta)
        CACHE_TEXTURAS_TEXTO[chave] = arcade.Texture(imagem)
    return CACHE_TEXTURAS_TEXTO[chave]


class TextoPixel:
    """
    Texto em pixel art que PODE MUDAR durante o jogo (pontuação, tempo,
    avisos, nome digitado). Guarda um sprite que é colocado na SpriteList
    recebida; o método definir() troca só a textura do sprite, e só quando
    o texto realmente mudou.

    `ancora` diz de onde vem a posição x: "esquerda" (borda esquerda do
    texto em x), "direita" (borda direita em x) ou "centro".
    """

    def __init__(self, lista: arcade.SpriteList, texto: str, tamanho: int,
                 escala: int, paleta: list, x: float, y: float,
                 ancora: str = "centro"):
        self.tamanho = tamanho
        self.escala = escala
        self.paleta = paleta
        self.x = x
        self.y = y
        self.ancora = ancora
        self.texto = texto

        self.sprite = arcade.Sprite(
            textura_pixel(texto, tamanho, escala, paleta))
        lista.append(self.sprite)
        self.posicionar()

    def posicionar(self):
        self.sprite.center_y = self.y
        if self.ancora == "esquerda":
            self.sprite.left = self.x
        elif self.ancora == "direita":
            self.sprite.right = self.x
        else:
            self.sprite.center_x = self.x

    def definir(self, texto: str, paleta: list = None):
        """Troca o texto (e, se quiser, as cores). Não faz nada se for igual."""
        if paleta is None:
            paleta = self.paleta
        if texto == self.texto and paleta is self.paleta:
            return
        self.texto = texto
        self.paleta = paleta
        self.sprite.texture = textura_pixel(
            texto, self.tamanho, self.escala, paleta)
        self.posicionar()


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
        # Impede o jogador de sair pelas laterais e pelo topo da tela
        # (antes dos return abaixo)
        if self.right > LARGURA:
            self.right = LARGURA
        if self.left < 0:
            self.left = 0
        if self.top > ALTURA:
            self.top = ALTURA
            if self.change_y > 0:
                self.change_y = 0     # bateu a cabeça no teto: para de subir

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
        self.coletavel = True     # Pode ser pega pela jogadora?


class MoedaPerdida(Moeda):
    """
    Morango que a jogadora perdeu ao ser envenenada. Ele sai dela, voa em
    arco até um ponto do mapa e, quando chega, vira uma Moeda comum.
    Enquanto voa, fica meio transparente e NÃO pode ser coletado.
    """

    def __init__(self, x_inicial: float, y_inicial: float,
                 x_final: float, y_final: float):
        super().__init__()
        self.x_inicial = x_inicial
        self.y_inicial = y_inicial
        self.x_final = x_final
        self.y_final = y_final
        self.tempo_voo = 0.0
        self.coletavel = False

        self.center_x = x_inicial
        self.center_y = y_inicial
        self.alpha = 150

    def update(self, delta_time: float = 1 / 60):
        # Depois que pousa, é só uma moeda parada
        if self.coletavel:
            return

        self.tempo_voo += delta_time
        # t vai de 0 (saiu da jogadora) até 1 (chegou ao destino)
        t = min(1.0, self.tempo_voo / DURACAO_VOO_MORANGO)

        # Posição em linha reta + um arco: 4 * t * (1 - t) vale 0 no
        # começo e no fim e 1 no meio do caminho.
        self.center_x = self.x_inicial + (self.x_final - self.x_inicial) * t
        self.center_y = (self.y_inicial + (self.y_final - self.y_inicial) * t
                         + ALTURA_ARCO_MORANGO * 4 * t * (1 - t))

        if t >= 1.0:
            self.coletavel = True
            self.alpha = 255


class MoedaEspecial(arcade.Sprite):
    """Moeda dinâmica: vale 5 pontos e rebate nas bordas da tela."""

    def __init__(self):
        super().__init__("cesta_strawberry.png", scale=0.035)
        self.valor = 5
        self.coletavel = True

    def update(self, delta_time: float = 1 / 60):
        # Física vetorial: posição += velocidade
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rebote: inverte o vetor (x -1) ao tocar a borda indo para fora
        if (self.left <= 0 and self.change_x < 0) or \
           (self.right >= LARGURA and self.change_x > 0):
            self.change_x *= -1

        if (self.bottom <= TOPO_CHAO and self.change_y < 0) or \
           (self.top >= ALTURA and self.change_y > 0):
            self.change_y *= -1


class Inimigo(arcade.Sprite):
    """
    Inimigo persistente (morango estragado): vaga sozinho pela tela,
    rebate nas bordas e NUNCA é removido ao tocar no jogador.
    """

    def __init__(self):
        super().__init__("strawberry_estragado.png", scale=1)

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if (self.left <= 0 and self.change_x < 0) or \
           (self.right >= LARGURA and self.change_x > 0):
            self.change_x *= -1

        if (self.bottom <= TOPO_CHAO and self.change_y < 0) or \
           (self.top >= ALTURA and self.change_y > 0):
            self.change_y *= -1


class InimigoEspecial(arcade.Sprite):
    """
    Bruxa voadora: persegue o jogador pelo ar (nos dois eixos, sem
    gravidade e sem física de plataforma) e se teletransporta para um
    ponto aleatório da tela depois de colidir.
    Tem animação (4 quadros em "vai e volta"), vira para o lado em que a
    jogadora está e balança de um lado para o outro enquanto voa.
    """

    def __init__(self, jogador: Player):
        # Quadros virados para a direita e versões espelhadas (esquerda)
        folha = arcade.load_spritesheet(ARQUIVO_BRUXA)
        quadros_direita = folha.get_texture_grid(
            size=(280, 270),
            columns=4,
            count=4
        )
        quadros_esquerda = []
        for quadro in quadros_direita:
            quadros_esquerda.append(quadro.flip_left_right())

        super().__init__(quadros_direita[0], scale=ESCALA_BRUXA)

        self.quadros_direita = quadros_direita
        self.quadros_esquerda = quadros_esquerda

        self.velocidade = VELOCIDADE_INIMIGO_ESPECIAL
        self.jogador = jogador   # Alvo da perseguição

        self.virada_para = "DIREITA"
        self.passo = 0                # posição dentro de ORDEM_VOO_BRUXA
        self.quadro_atual = 0         # quadro (0 a 3) mostrado agora
        self.tempo_animacao = 0.0
        self.tempo_balanco = 0.0

    def update(self, delta_time: float = 1 / 60):
        # Vetor da bruxa até a jogadora. Dividir pela distância deixa o
        # vetor com tamanho 1, então ela voa sempre na mesma velocidade,
        # inclusive na diagonal.
        dx = self.jogador.center_x - self.center_x
        dy = self.jogador.center_y - self.center_y
        distancia = math.hypot(dx, dy)

        if distancia > self.velocidade:
            self.change_x = dx / distancia * self.velocidade
            self.change_y = dy / distancia * self.velocidade
        else:
            self.change_x = 0
            self.change_y = 0

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Balanço de um lado para o outro (seno vai e volta entre -1 e 1)
        self.tempo_balanco += delta_time
        self.center_x += math.sin(self.tempo_balanco * 4) * BALANCO_BRUXA

        # Mantém a bruxa dentro da tela e acima do chão
        if self.left < 0:
            self.left = 0
        if self.right > LARGURA:
            self.right = LARGURA
        if self.top > ALTURA:
            self.top = ALTURA
        if self.bottom < TOPO_CHAO:
            self.bottom = TOPO_CHAO

        # Vira para o lado da jogadora (com uma folga para não ficar
        # trocando de lado quando ela está bem em cima)
        if dx > 4:
            self.virada_para = "DIREITA"
        elif dx < -4:
            self.virada_para = "ESQUERDA"

        # Animação: troca de quadro a cada TEMPO_QUADRO_BRUXA segundos,
        # seguindo a ordem 0,1,2,3,2,1 (vai e volta, sem pulo brusco)
        self.tempo_animacao += delta_time
        if self.tempo_animacao >= TEMPO_QUADRO_BRUXA:
            self.tempo_animacao -= TEMPO_QUADRO_BRUXA
            self.passo = (self.passo + 1) % len(ORDEM_VOO_BRUXA)
            self.quadro_atual = ORDEM_VOO_BRUXA[self.passo]

        if self.virada_para == "DIREITA":
            self.texture = self.quadros_direita[self.quadro_atual]
        else:
            self.texture = self.quadros_esquerda[self.quadro_atual]

    def teletransportar(self):
        """Renasce em um ponto aleatório do céu, longe da jogadora."""
        for _ in range(50):
            x = random.randint(60, LARGURA - 60)
            y = random.randint(TOPO_CHAO + 60, ALTURA - 60)
            distancia = math.hypot(x - self.jogador.center_x,
                                   y - self.jogador.center_y)
            if distancia > 250:
                break

        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0


class BarraVida:
    """
    Barra de vidas no canto superior direito: um coração por vida.
    Cada vida perdida troca o coração cheio por um vazio, da direita
    para a esquerda.
    """

    def __init__(self, vidas_max: int):
        self.textura_cheio = arcade.load_texture(ARQUIVO_CORACAO_CHEIO)
        self.textura_vazio = arcade.load_texture(ARQUIVO_CORACAO_VAZIO)

        self.coracoes = arcade.SpriteList()
        for indice in range(vidas_max):
            coracao = arcade.Sprite(self.textura_cheio)
            # O último coração fica encostado na borda direita da tela
            posicoes_ate_o_fim = vidas_max - 1 - indice
            coracao.right = LARGURA - 10 - posicoes_ate_o_fim * (coracao.width + 6)
            coracao.top = ALTURA - 10
            self.coracoes.append(coracao)

    def atualizar(self, vidas: int):
        """Deixa cheios os primeiros `vidas` corações e esvazia o resto."""
        for indice, coracao in enumerate(self.coracoes):
            if indice < vidas:
                coracao.texture = self.textura_cheio
            else:
                coracao.texture = self.textura_vazio

    def desenhar(self):
        self.coracoes.draw()


class Explosao(arcade.Sprite):
    """
    Efeito de explosão animado por spritesheet.
    Toca a animação uma única vez e se remove sozinho ao terminar.
    """

    def __init__(self, x: float, y: float, quadros: list, scale: float = 1.0):
        super().__init__(quadros[0], scale=scale)
        self.center_x = x
        self.center_y = y
        self.quadros = quadros          # Lista de texturas já fatiadas
        self.quadro_atual = 0
        self.tempo_animacao = 0.0

    def update(self, delta_time: float = 1 / 60):
        self.tempo_animacao += delta_time
        if self.tempo_animacao >= 0.06:      # Troca de quadro a cada 60 ms
            self.tempo_animacao = 0.0
            self.quadro_atual += 1
            if self.quadro_atual >= len(self.quadros):
                self.remove_from_sprite_lists()   # Fim da animação
                return
            self.texture = self.quadros[self.quadro_atual]


class NuvemVeneno(arcade.Sprite):
    """
    Animação de veneno: uma nuvem de gás com bolhas e uma caveira que
    acompanha a jogadora enquanto ela está envenenada.
    Diferente da Explosao (que toca uma vez e some), esta animação fica em
    ciclo; quem decide quando ela acaba é a TelaJogo, junto com o veneno.
    """

    def __init__(self, quadros: list, jogador: arcade.Sprite):
        super().__init__(quadros[0], scale=ESCALA_NUVEM_VENENO)
        self.quadros = quadros
        self.jogador = jogador          # Quem ela acompanha
        self.quadro_atual = 0
        self.tempo_animacao = 0.0
        self.center_x = jogador.center_x
        self.center_y = jogador.center_y

    def update(self, delta_time: float = 1 / 60):
        # Acompanha a jogadora
        self.center_x = self.jogador.center_x
        self.center_y = self.jogador.center_y

        # Troca de quadro a cada 80 ms e volta ao primeiro no fim (ciclo)
        self.tempo_animacao += delta_time
        if self.tempo_animacao >= 0.08:
            self.tempo_animacao = 0.0
            self.quadro_atual = (self.quadro_atual + 1) % len(self.quadros)
            self.texture = self.quadros[self.quadro_atual]


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

    def desenhar_painel(self, centro_y: float, altura: float, largura: float = 740):
        """Painel escuro com borda amarela e vermelha, para dar leitura ao texto."""
        retangulo = arcade.XYWH(LARGURA / 2, centro_y, largura, altura)
        arcade.draw_rect_filled(retangulo, (40, 8, 14, 195))
        arcade.draw_rect_outline(retangulo, (255, 200, 30), border_width=4)
        externo = arcade.XYWH(LARGURA / 2, centro_y, largura + 8, altura + 8)
        arcade.draw_rect_outline(externo, (205, 35, 35), border_width=4)


# ==========================================
# TELA INICIAL
# ==========================================
class TelaInicial(TelaComFundo):
    def __init__(self):
        super().__init__()

        # Título e opções são imagens PNG pixeladas, guardadas em sprites
        self.sprite_textos = arcade.SpriteList()

        titulo = arcade.Sprite(ARQUIVO_TITULO)
        titulo.center_x = LARGURA / 2
        titulo.center_y = 485
        self.sprite_textos.append(titulo)

        for indice, arquivo in enumerate(ARQUIVOS_MENU):
            opcao = arcade.Sprite(arquivo)
            opcao.center_x = LARGURA / 2
            opcao.center_y = 340 - indice * 58
            self.sprite_textos.append(opcao)

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()
        self.sprite_textos.draw()

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
    def __init__(self):
        super().__init__()

        if PULO_DUPLO:
            texto_pulo = "W, ↑ ou ESPAÇO: pular. De novo no ar: pulo duplo!"
        else:
            texto_pulo = "W, ↑ ou ESPAÇO: pular (sem pulo duplo)."

        # (texto, paleta de cores). Os textos usam as constantes do jogo,
        # então se você mudar VIDAS ou TEMPO_PARALISIA o texto muda junto.
        linhas = [
            ("OBJETIVO: colete todas as moedas do cenário.", PALETA_TEXTO),
            ("A / D ou ← →: andar para os lados.", PALETA_TEXTO),
            (texto_pulo, PALETA_TEXTO),
            ("Morango: +1 ponto.  Cesta: +5 pontos (ela quica!)", PALETA_TEXTO),
            ("Morango estragado: -1 ponto e veneno!", PALETA_VERDE),
            (f"Envenenada, você fica paralisada por {TEMPO_PARALISIA:.0f} s.", PALETA_VERDE),
            ("O ponto vira um morango no mapa: pegue de volta!", PALETA_VERDE),
            (f"Bruxa: voa atrás de você e tira 1 vida (são {VIDAS}).", PALETA_MENU),
            ("Sem vidas, o jogo acaba.", PALETA_MENU),
            ("Depois de um golpe, você fica imune por 1,5 s.", PALETA_TEXTO),
            ("Escape de todos os inimigos: pontuação máxima!", PALETA_OURO),
        ]

        self.sprite_textos = arcade.SpriteList()
        self.sprite_textos.append(
            sprite_texto("INSTRUÇÕES", 16, 3, PALETA_TITULO, LARGURA / 2, 550))
        for indice, (texto, paleta) in enumerate(linhas):
            self.sprite_textos.append(
                sprite_texto(texto, 10, 2, paleta, LARGURA / 2, 480 - indice * 33))
        self.sprite_textos.append(
            sprite_texto("Pressione ESC ou M para voltar", 11, 2, PALETA_MENU,
                         LARGURA / 2, 58))

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()
        self.desenhar_painel(centro_y=305, altura=400)
        self.sprite_textos.draw()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ESCAPE, arcade.key.M):
            self.window.show_view(TelaInicial())


# ==========================================
# TELA SOBRE O JOGO
# ==========================================
class TelaSobre(TelaComFundo):
    def __init__(self):
        super().__init__()

        # Textos em pixel art e avatares: tudo sprite, em SpriteLists
        self.sprite_textos = arcade.SpriteList()
        self.sprite_avatares = arcade.SpriteList()

        self.sprite_textos.append(
            sprite_texto("SOBRE O JOGO", 16, 3, PALETA_TITULO, LARGURA / 2, 550))
        self.sprite_textos.append(
            sprite_texto("Moranguinho: um jogo de plataforma", 11, 2, PALETA_TEXTO,
                         LARGURA / 2, 465))
        self.sprite_textos.append(
            sprite_texto("feito com Python Arcade e POO.", 11, 2, PALETA_TEXTO,
                         LARGURA / 2, 430))
        self.sprite_textos.append(
            sprite_texto("Desenvolvido por:", 12, 2, PALETA_MENU, LARGURA / 2, 380))
        self.sprite_textos.append(
            sprite_texto("Pressione ESC ou M para voltar", 11, 2, PALETA_MENU,
                         LARGURA / 2, 58))

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

            self.sprite_textos.append(
                sprite_texto(nome, 12, 2, PALETA_OURO, x, 170))

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()
        self.desenhar_painel(centro_y=305, altura=400)
        self.sprite_avatares.draw()
        self.sprite_textos.draw()

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

        # Vidas (a bruxa tira vidas; o morango estragado tira pontos)
        self.vidas = VIDAS
        self.barra_vida = BarraVida(VIDAS)

        # Quantos pulos já foram dados desde que saiu do chão (0, 1 ou 2)
        self.pulos_dados = 0

        # Temporizadores dos efeitos de colisão (zero = efeito desligado)
        self.tempo_invencivel = 0.0
        self.tempo_flash = 0.0
        self.tempo_tremor = 0.0

        # Veneno do morango estragado
        self.tempo_veneno = 0.0       # segundos restantes de veneno
        self.tempo_paralisia = 0.0    # segundos restantes de paralisia
        self.golpes_morango = 0       # quantas vezes o morango estragado pegou
        self.nuvem_veneno = None      # animação de veneno (None = sem veneno)

        # Cor do clarão: vermelho (bruxa) ou verde (veneno)
        self.cor_flash = COR_FLASH_BRUXA

        # Textos do HUD em pixel art. Cada TextoPixel só gera imagem nova
        # quando o texto muda. Ficam em listas separadas porque alguns só
        # aparecem em certos momentos (veneno, paralisia e aviso).
        self.lista_hud = arcade.SpriteList()
        self.txt_pontos = TextoPixel(self.lista_hud, "PONTOS: 0", 11, 2,
                                     PALETA_OURO, 12, 572, "esquerda")
        self.txt_tempo = TextoPixel(self.lista_hud, "TEMPO: 0s", 11, 2,
                                    PALETA_OURO, 12, 538, "esquerda")

        self.lista_veneno = arcade.SpriteList()
        self.txt_veneno = TextoPixel(self.lista_veneno, "ENVENENADA! 3.0s", 11, 2,
                                     PALETA_VERDE, LARGURA / 2 - 15, 572)

        self.lista_paralisia = arcade.SpriteList()
        self.txt_paralisia = TextoPixel(self.lista_paralisia, "PARALISADA!", 11, 2,
                                        PALETA_VERDE, LARGURA / 2 - 15, 538)

        self.lista_aviso = arcade.SpriteList()
        self.txt_aviso = TextoPixel(self.lista_aviso, "AVISO", 12, 2,
                                    PALETA_TITULO, LARGURA / 2, 490)

        # Câmera do mundo do jogo: é ela que treme. O HUD e o clarão
        # são desenhados com a câmera padrão da janela, que fica parada.
        self.camera = arcade.Camera2D()

        # Aumenta o fundo para a câmera tremer sem mostrar bordas vazias
        for fundo in self.background_list:
            fundo.width = LARGURA + 2 * INTENSIDADE_TREMOR
            fundo.height = ALTURA + 2 * INTENSIDADE_TREMOR

        # Teclas de movimento atualmente seguradas
        self.teclas = set()

        self.sprite_blocos = arcade.SpriteList()
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_inimigo_persistente = arcade.SpriteList()
        self.sprite_inimigo_especial = arcade.SpriteList()
        self.sprite_moedas = arcade.SpriteList()
        self.sprite_efeitos = arcade.SpriteList()

        # Quadros da explosão: carregados UMA vez e reaproveitados a cada golpe
        folha_explosao = arcade.load_spritesheet(ARQUIVO_EXPLOSAO)
        self.quadros_explosao = folha_explosao.get_texture_grid(
            size=(128, 128),
            columns=6,
            count=6
        )

        # Quadros da animação de veneno: também carregados uma vez só
        folha_veneno = arcade.load_spritesheet(ARQUIVO_VENENO)
        self.quadros_veneno = folha_veneno.get_texture_grid(
            size=(128, 128),
            columns=6,
            count=6
        )

        self.criar_cenario()
        self.criar_personagens()
        self.criar_moedas()

        # Pontuação máxima = soma do valor de todas as moedas
        self.pontuacao_maxima = 0
        for moeda in self.sprite_moedas:
            self.pontuacao_maxima += moeda.valor

        # Motor de física da jogadora (a bruxa voa, então não usa motor)
        self.engine_jogador = arcade.PhysicsEnginePlatformer(
            player_sprite=self.jogador,
            walls=self.sprite_blocos,
            gravity_constant=GRAVIDADE
        )

    # ---------- construção do cenário ----------
    def criar_cenario(self):
        # Chão: uma fileira de blocos com o TOPO em TOPO_CHAO. Ela é invisível
        # (alpha 0): o chão que aparece é o desenhado no fundo.png, e os
        # blocos só fazem a colisão (física e can_jump) acontecer nele.
        for x in range(TAMANHO_BLOCO // 2, LARGURA + TAMANHO_BLOCO, TAMANHO_BLOCO):
            chao = Bloco(x, TOPO_CHAO - TAMANHO_BLOCO / 2)
            chao.alpha = 0
            self.sprite_blocos.append(chao)

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

        # Inimigo especial (bruxa voadora que persegue pelo ar)
        self.bruxa = InimigoEspecial(self.jogador)
        self.bruxa.center_x = 600
        self.bruxa.center_y = 450
        self.sprite_inimigo_especial.append(self.bruxa)

    def sortear_posicao_moeda(self, moeda, outras, longe_de=None):
        """
        Escolhe uma posição para a moeda bem afastada das outras.
        Sorteia vários candidatos (fora dos blocos) e fica com o que tem a
        MAIOR distância até a moeda mais próxima. Assim as moedas se
        espalham pelo mapa em vez de formar grupos.
        `longe_de` (opcional) é um sprite do qual também queremos ficar longe.
        """
        melhor_x = None
        melhor_y = None
        melhor_distancia = -1

        for _ in range(CANDIDATOS_MORANGO):
            x = random.randint(MARGEM_MORANGO, LARGURA - MARGEM_MORANGO)
            y = random.randint(TOPO_CHAO + 40, ALTURA_MAX_MORANGO)
            moeda.center_x = x
            moeda.center_y = y

            # Descarta candidatos que caíram dentro de um bloco
            if arcade.check_for_collision_with_list(moeda, self.sprite_blocos):
                continue

            # Distância até a moeda mais próxima (e até o sprite a evitar)
            distancia = 9999
            for outra in outras:
                distancia = min(distancia,
                                math.hypot(outra.center_x - x, outra.center_y - y))
            if longe_de is not None:
                distancia = min(distancia,
                                math.hypot(longe_de.center_x - x,
                                           longe_de.center_y - y))

            if distancia > melhor_distancia:
                melhor_distancia = distancia
                melhor_x = x
                melhor_y = y

        # Se todos os candidatos caíram em blocos (raro), usa um ponto do chão
        if melhor_x is None:
            melhor_x = random.randint(MARGEM_MORANGO, LARGURA - MARGEM_MORANGO)
            melhor_y = TOPO_CHAO + 60

        moeda.center_x = melhor_x
        moeda.center_y = melhor_y

    def criar_moedas(self):
        # 25 moedas comuns bem espalhadas e alcançáveis com os pulos
        for _ in range(25):
            moeda = Moeda()
            self.sortear_posicao_moeda(moeda, self.sprite_moedas)
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

        # Mundo do jogo: desenhado pela câmera que pode tremer
        self.camera.use()
        self.desenhar_fundo()

        self.sprite_blocos.draw()
        self.sprite_moedas.draw()
        self.sprite_inimigo_persistente.draw()
        self.sprite_inimigo_especial.draw()
        self.sprite_jogador.draw()
        self.sprite_efeitos.draw()      # Explosão por cima de tudo

        # Câmera padrão da janela (parada): clarão e HUD não tremem
        self.window.default_camera.use()

        # Clarão (vermelho da bruxa ou verde do veneno): o alpha diminui
        # junto com o tempo restante
        if self.tempo_flash > 0:
            alpha = int(120 * self.tempo_flash / TEMPO_FLASH)
            r, g, b = self.cor_flash
            arcade.draw_rect_filled(
                arcade.XYWH(LARGURA / 2, ALTURA / 2, LARGURA, ALTURA),
                (r, g, b, alpha)
            )

        # HUD em pixel art: o texto é atualizado só se mudou
        self.atualizar_textos_hud()
        self.lista_hud.draw()

        # Veneno e paralisia (verde): só aparecem enquanto durarem
        if self.tempo_veneno > 0:
            self.lista_veneno.draw()
        if self.tempo_paralisia > 0:
            self.lista_paralisia.draw()

        # Aviso do golpe: só aparece enquanto a jogadora está imune
        if self.tempo_invencivel > 0:
            self.lista_aviso.draw()

        # Vidas em corações (canto superior direito)
        self.barra_vida.desenhar()

    def atualizar_textos_hud(self):
        """Atualiza os textos do HUD (cada um só troca de imagem se mudou)."""
        self.txt_pontos.definir(f"PONTOS: {self.pontuacao}")
        self.txt_tempo.definir(f"TEMPO: {int(self.tempo_decorrido)}s")
        if self.tempo_veneno > 0:
            self.txt_veneno.definir(f"ENVENENADA! {self.tempo_veneno:.1f}s")

    # ---------- lógica ----------
    def levar_golpe(self, aviso: str, cor_flash: tuple, paleta_aviso: list):
        """
        Liga os efeitos comuns a qualquer golpe: imunidade com piscar,
        clarão colorido, tremor de tela e aviso em pixel art. O efeito de
        animação (explosão ou veneno) é criado por quem chama.
        """
        self.txt_aviso.definir(aviso, paleta_aviso)
        self.cor_flash = cor_flash
        self.tempo_invencivel = TEMPO_INVENCIVEL
        self.tempo_flash = TEMPO_FLASH
        self.tempo_tremor = TEMPO_TREMOR

    def explodir(self, inimigo: arcade.Sprite):
        """Explosão no ponto de impacto (média entre os centros)."""
        x = (self.jogador.center_x + inimigo.center_x) / 2
        y = (self.jogador.center_y + inimigo.center_y) / 2
        self.sprite_efeitos.append(Explosao(x, y, self.quadros_explosao))

    def envenenar(self):
        """
        Liga o veneno: a jogadora fica verde, paralisada, e a animação de
        veneno passa a acompanhá-la. Se já estava envenenada, só reinicia
        os tempos.
        """
        self.tempo_veneno = TEMPO_VENENO
        if self.nuvem_veneno is None:
            self.nuvem_veneno = NuvemVeneno(self.quadros_veneno, self.jogador)
            self.sprite_efeitos.append(self.nuvem_veneno)

        # Paralisa: para de andar na hora
        self.tempo_paralisia = TEMPO_PARALISIA
        self.jogador.change_x = 0

    def derrubar_morango(self):
        """
        O ponto perdido vira um morango que sai da jogadora e voa até um
        ponto bem afastado das outras moedas (e dela).
        """
        destino = Moeda()   # só serve para testar o ponto de destino
        fixas = []
        for moeda in self.sprite_moedas:
            if not isinstance(moeda, MoedaEspecial):
                fixas.append(moeda)
        self.sortear_posicao_moeda(destino, fixas, longe_de=self.jogador)

        perdida = MoedaPerdida(
            self.jogador.center_x, self.jogador.center_y,
            destino.center_x, destino.center_y
        )
        self.sprite_moedas.append(perdida)

    def dano_morango(self):
        """
        O morango estragado tira 1 PONTO, envenena e paraliza a jogadora e
        faz um morango cair no mapa.
        """
        self.pontuacao -= 1
        self.golpes_morango += 1
        self.envenenar()
        self.derrubar_morango()
        # Sem explosão: o efeito aqui é a animação de veneno e o clarão verde
        self.levar_golpe("ENVENENADA! -1 PONTO", COR_FLASH_VENENO, PALETA_VERDE)

    def dano_bruxa(self):
        """A bruxa tira 1 VIDA."""
        self.vidas -= 1
        self.barra_vida.atualizar(self.vidas)
        self.explodir(self.bruxa)
        self.levar_golpe("A BRUXA PEGOU VOCÊ! -1 VIDA", COR_FLASH_BRUXA,
                         PALETA_TITULO)

    def pular(self):
        """
        Pulo normal (do chão) e pulo duplo (no ar). A altura do pulo normal
        é 75% da altura do pulo duplo. Paralisada, não pula.
        """
        if self.tempo_paralisia > 0:
            return          # paralisada: não pula

        if self.engine_jogador.can_jump():
            # Apoiada em um bloco: pulo normal
            self.jogador.change_y = FORCA_PULO_NORMAL
            self.pulos_dados = 1
        elif PULO_DUPLO and self.pulos_dados < 2:
            # No ar e ainda com pulo sobrando: pulo duplo
            self.jogador.change_y = FORCA_PULO
            self.pulos_dados = 2

    def on_update(self, delta_time):
        # Cronômetro
        self.tempo_decorrido += delta_time

        # Paralisada: não anda (a gravidade do motor continua valendo)
        if self.tempo_paralisia > 0:
            self.jogador.change_x = 0

        # Motor de física da jogadora: gravidade, movimento e colisão com os blocos
        self.engine_jogador.update()

        # De volta ao chão: os pulos ficam disponíveis de novo
        if self.engine_jogador.can_jump():
            self.pulos_dados = 0

        # Cada lista chama o update() de cada sprite (polimorfismo):
        # animação da jogadora, moedas, inimigos e explosões
        self.sprite_jogador.update(delta_time)
        self.sprite_moedas.update(delta_time)
        self.sprite_inimigo_persistente.update(delta_time)
        self.sprite_inimigo_especial.update(delta_time)
        self.sprite_efeitos.update(delta_time)

        # Desconta o tempo dos efeitos (nunca abaixo de zero)
        self.tempo_invencivel = max(0.0, self.tempo_invencivel - delta_time)
        self.tempo_flash = max(0.0, self.tempo_flash - delta_time)
        self.tempo_tremor = max(0.0, self.tempo_tremor - delta_time)
        self.tempo_veneno = max(0.0, self.tempo_veneno - delta_time)

        # Fim da paralisia: volta a obedecer as teclas que ainda estão seguradas
        if self.tempo_paralisia > 0:
            self.tempo_paralisia = max(0.0, self.tempo_paralisia - delta_time)
            if self.tempo_paralisia == 0:
                self.atualizar_direcao()

        # O veneno acabou: tira a animação de veneno de cima da jogadora
        if self.tempo_veneno == 0 and self.nuvem_veneno is not None:
            self.nuvem_veneno.remove_from_sprite_lists()
            self.nuvem_veneno = None

        # Coleta de moedas (o morango perdido só vale depois que pousar)
        moedas_coletadas = arcade.check_for_collision_with_list(
            self.jogador, self.sprite_moedas
        )
        for moeda in moedas_coletadas:
            if not moeda.coletavel:
                continue
            self.pontuacao += moeda.valor
            moeda.remove_from_sprite_lists()

        # Colisão com o inimigo persistente: NÃO é removido. Só tira ponto
        # se a jogadora não estiver imune (a imunidade evita o dano repetido
        # enquanto os dois continuam encostados).
        if self.tempo_invencivel == 0:
            if arcade.check_for_collision(self.jogador, self.inimigo_persistente):
                self.dano_morango()

        # Colisão com a bruxa: ela SEMPRE se teletransporta. A vida só é
        # tirada se a jogadora não estiver imune.
        if arcade.check_for_collision(self.jogador, self.bruxa):
            if self.tempo_invencivel == 0:
                self.dano_bruxa()
            self.bruxa.teletransportar()

        # Aparência da jogadora: o piscar muda a transparência (alpha) a cada
        # décimo de segundo e o veneno tinge de verde (cor R, G, B).
        if self.tempo_invencivel > 0 and int(self.tempo_invencivel * 10) % 2 == 0:
            alpha = 80
        else:
            alpha = 255

        if self.tempo_veneno > 0:
            r, g, b = COR_VENENO
        else:
            r, g, b = 255, 255, 255     # cor original da imagem

        self.jogador.color = (r, g, b, alpha)

        # Tremor: a câmera sacode com força decrescente e volta ao centro
        if self.tempo_tremor > 0:
            forca = INTENSIDADE_TREMOR * self.tempo_tremor / TEMPO_TREMOR
            self.camera.position = (
                LARGURA / 2 + random.uniform(-forca, forca),
                ALTURA / 2 + random.uniform(-forca, forca),
            )
        else:
            self.camera.position = (LARGURA / 2, ALTURA / 2)

        # Fim de jogo: sem vidas (derrota) ou todas as moedas coletadas (vitória)
        if self.vidas <= 0 or len(self.sprite_moedas) == 0:
            self.window.show_view(
                TelaGameOver(
                    self.pontuacao,
                    self.tempo_decorrido,
                    self.pontuacao_maxima,
                    self.vidas,
                    self.golpes_morango == 0
                )
            )

    # ---------- teclado ----------
    def atualizar_direcao(self):
        # Paralisada: ignora as setas (elas continuam registradas em
        # self.teclas, então ao fim da paralisia ela volta a andar)
        if self.tempo_paralisia > 0:
            self.jogador.change_x = 0
            return

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

        # Pulo: normal no chão e duplo no ar (a regra está em pular())
        elif key in (arcade.key.W, arcade.key.UP, arcade.key.SPACE):
            self.pular()

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
    def __init__(self, pontuacao: int, tempo_jogo: float, pontuacao_maxima: int,
                 vidas: int = VIDAS, sem_dano: bool = True):
        super().__init__()

        self.pontuacao = pontuacao
        self.tempo_jogo = tempo_jogo
        self.pontuacao_maxima = pontuacao_maxima
        self.vidas = vidas
        # False se o morango estragado pegou a jogadora em algum momento
        # (o morango perdido devolve o ponto, então a pontuação sozinha
        # não mostra que ela levou dano)
        self.sem_dano = sem_dano

        # Fase 1 ("nome"): o jogador digita o nome.
        # Fase 2 ("opcoes"): mostra [M], [R] e [ESC].
        self.fase = "nome"
        self.nome_digitado = ""
        self.id_salvo = None      # id do registro criado no banco
        self.erro_banco = False

        # Derrota: acabaram as vidas. Vitória: coletou todas as moedas.
        # "Perfeito" = pontuação máxima, nenhuma vida perdida e nenhum
        # golpe do morango estragado.
        self.venceu = self.vidas > 0
        self.perfeito = (self.venceu
                         and self.pontuacao == self.pontuacao_maxima
                         and self.vidas == VIDAS
                         and self.sem_dano)

        # Título pixelado conforme o resultado
        if not self.venceu:
            arquivo_banner = ARQUIVO_FIM_DERROTA
        elif self.perfeito:
            arquivo_banner = ARQUIVO_FIM_PERFEITO
        else:
            arquivo_banner = ARQUIVO_FIM_VITORIA

        self.sprite_banner = arcade.SpriteList()
        banner = arcade.Sprite(arquivo_banner)
        banner.center_x = LARGURA / 2
        banner.center_y = 510
        self.sprite_banner.append(banner)

        # Textos em pixel art, em três listas: os que aparecem sempre, os
        # da fase do nome e os da fase das opções.
        self.lista_comum = arcade.SpriteList()
        self.lista_nome = arcade.SpriteList()
        self.lista_opcoes = arcade.SpriteList()

        TextoPixel(self.lista_comum, f"PONTUAÇÃO FINAL: {self.pontuacao}",
                   14, 2, PALETA_OURO, LARGURA / 2, 412)
        if self.perfeito:
            TextoPixel(self.lista_comum, f"TEMPO TOTAL: {self.tempo_jogo:.1f}s",
                       11, 2, PALETA_TEXTO, LARGURA / 2, 376)
            TextoPixel(self.lista_comum,
                       "Você escapou de todos os inimigos perfeitamente!",
                       10, 2, PALETA_OURO, LARGURA / 2, 344)

        # Fase 1: digitar o nome
        TextoPixel(self.lista_nome, "Digite seu nome para o ranking:",
                   11, 2, PALETA_TEXTO, LARGURA / 2, 295)
        self.txt_nome = TextoPixel(self.lista_nome, "_", 14, 2, PALETA_OURO,
                                   LARGURA / 2, 240)
        TextoPixel(self.lista_nome, "[ENTER] Salvar     [ESC] Pular",
                   11, 2, PALETA_MENU, LARGURA / 2, 160)

        # Fase 2: mensagem sobre o salvamento e as opções
        self.txt_mensagem = TextoPixel(self.lista_opcoes,
                                       "Pontuação salva no ranking!",
                                       12, 2, PALETA_OURO, LARGURA / 2, 295)
        TextoPixel(self.lista_opcoes, "[M] Menu", 12, 2, PALETA_MENU, 170, 200)
        TextoPixel(self.lista_opcoes, "[R] Ranking", 12, 2, PALETA_MENU, 400, 200)
        TextoPixel(self.lista_opcoes, "[ESC] Sair", 12, 2, PALETA_MENU, 630, 200)

    def salvar_pontuacao(self, nome: str):
        """Único ponto desta tela que conversa com o banco."""
        return Pontuacao.create(
            nome_jogador=nome,
            pontos=self.pontuacao,
            tempo_partida=self.tempo_jogo
        )

    def ir_para_opcoes(self):
        """Passa para a fase 2 e escolhe a mensagem sobre o salvamento."""
        self.fase = "opcoes"
        if self.erro_banco:
            self.txt_mensagem.definir("Não foi possível salvar no ranking.",
                                      PALETA_MENU)
        elif self.id_salvo is not None:
            self.txt_mensagem.definir("Pontuação salva no ranking!", PALETA_OURO)
        else:
            self.txt_mensagem.definir("Pontuação não salva.", PALETA_TEXTO)

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        self.sprite_banner.draw()
        self.desenhar_painel(centro_y=275, altura=340)
        self.lista_comum.draw()

        if self.fase == "nome":
            # Caixa onde o nome aparece (o "_" é o cursor)
            caixa = arcade.XYWH(LARGURA / 2, 240, 400, 56)
            arcade.draw_rect_filled(caixa, (20, 4, 8, 230))
            arcade.draw_rect_outline(caixa, (255, 200, 30), border_width=3)
            self.txt_nome.definir(self.nome_digitado + "_")
            self.lista_nome.draw()
        else:
            self.lista_opcoes.draw()

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
                    self.ir_para_opcoes()

            elif key == arcade.key.ESCAPE:
                self.ir_para_opcoes()   # Pula sem salvar

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

        # Textos fixos em pixel art (criados uma vez)
        self.sprite_textos = arcade.SpriteList()
        self.sprite_textos.append(
            sprite_texto("RANKING - TOP 10", 16, 3, PALETA_OURO, LARGURA / 2, 553))
        self.sprite_textos.append(
            sprite_texto("[J] Jogar     [ESC] ou [M] Menu", 11, 2, PALETA_MENU,
                         LARGURA / 2, 50))

        if len(self.melhores) == 0:
            # Banco ainda sem pontuações
            self.sprite_textos.append(
                sprite_texto("Nenhuma pontuação ainda! Seja o primeiro.", 11, 2,
                             PALETA_TEXTO, LARGURA / 2, 300))
        else:
            # Cabeçalho das colunas (alinhado à esquerda ou à direita)
            cabecalhos = [
                ("POS", "left", 100), ("JOGADOR", "left", 160),
                ("PONTOS", "right", 450), ("TEMPO", "right", 560),
                ("DATA", "right", 700),
            ]
            for texto, lado, x in cabecalhos:
                cab = sprite_texto(texto, 9, 2, PALETA_MENU, x, 482)
                if lado == "left":
                    cab.left = x
                else:
                    cab.right = x
                self.sprite_textos.append(cab)

    def texto_sombra(self, texto, x, y, cor, tamanho=16, **extras):
        """draw_text com uma sombra escura embaixo (mesmo ar dos títulos)."""
        arcade.draw_text(texto, x + 2, y - 2, (45, 8, 12), tamanho, bold=True, **extras)
        arcade.draw_text(texto, x, y, cor, tamanho, bold=True, **extras)

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()
        self.desenhar_painel(centro_y=300, altura=420, largura=700)
        self.sprite_textos.draw()

        # enumerate dá o índice; o Y é proporcional a ele
        medalhas = [(255, 215, 0), (215, 215, 225), (205, 127, 50)]
        for indice, p in enumerate(self.melhores):
            y = 445 - indice * 34

            if p.id == self.destaque_id:
                # Faixa amarela atrás da partida recém-salva
                arcade.draw_rect_filled(
                    arcade.XYWH(LARGURA / 2, y + 8, 660, 30), (255, 200, 30, 80))
                cor = (255, 240, 60)
                cor_pos = cor
            else:
                cor = (255, 244, 220)
                cor_pos = medalhas[indice] if indice < 3 else cor

            self.texto_sombra(f"{indice + 1}º", 100, y, cor_pos)
            self.texto_sombra(p.nome_jogador, 160, y, cor)
            self.texto_sombra(str(p.pontos), 450, y, cor, anchor_x="right")
            self.texto_sombra(f"{p.tempo_partida:.1f}s", 560, y, cor, anchor_x="right")
            self.texto_sombra(p.data_hora.strftime("%d/%m/%Y"), 700, y, cor,
                              anchor_x="right")

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