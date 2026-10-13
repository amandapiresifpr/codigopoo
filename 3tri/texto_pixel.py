"""
Texto em pixel art (vermelho e amarelo) usado pelo jogo e pelo gerador de PNGs.
Renderiza o texto pequeno, sem suavização, e amplia com NEAREST: o resultado
tem pixels grandes e visíveis, com contorno escuro e sombra.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PASTA = os.path.dirname(os.path.abspath(__file__))
CANDIDATAS = [
    os.path.join(PASTA, "DejaVuSans-Bold.ttf"),   # vem junto com o jogo
    "DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

CONTORNO = (45, 8, 12, 255)

PALETA_TITULO = [(255, 240, 120), (255, 214, 30), (255, 150, 20), (240, 50, 30), (200, 20, 30)]
PALETA_AMARELA = [(255, 240, 120), (255, 214, 30), (255, 214, 30), (235, 170, 20)]
PALETA_MENU = [(255, 232, 80), (255, 200, 30), (250, 120, 25), (225, 40, 30)]
PALETA_DERROTA = [(255, 120, 90), (240, 50, 40), (200, 20, 30), (150, 10, 25)]
PALETA_OURO = [(255, 250, 170), (255, 225, 50), (255, 185, 20), (225, 130, 15)]
PALETA_TEXTO = [(255, 246, 200), (255, 236, 150), (255, 220, 90), (250, 190, 60)]
PALETA_VERDE = [(210, 255, 150), (150, 240, 90), (90, 200, 60), (60, 150, 50)]


def _fonte(tamanho):
    for caminho in CANDIDATAS:
        try:
            return ImageFont.truetype(caminho, tamanho)
        except OSError:
            continue
    return ImageFont.load_default()


def _mascara(texto, tamanho):
    fonte = _fonte(tamanho)
    caixa = fonte.getbbox(texto)

    # Tela com folga: o modo "1" (sem suavização) desenha o texto um pouco
    # mais largo do que o getbbox mede, então não dá para confiar nele.
    largura = (caixa[2] - caixa[0]) * 2 + 2 * tamanho
    altura = (caixa[3] - caixa[1]) + 2 * tamanho
    img = Image.new("L", (largura, altura), 0)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"                      # sem suavização: pixels nítidos
    d.text((tamanho - caixa[0], tamanho - caixa[1]), texto, font=fonte, fill=255)
    img = img.point(lambda v: 255 if v > 127 else 0)

    # Recorta exatamente em volta do que foi desenhado (1 px de borda)
    ink = img.getbbox()
    if ink is None:                       # texto vazio ou só espaços
        return Image.new("L", (3, 3), 0)
    return img.crop((ink[0] - 1, ink[1] - 1, ink[2] + 1, ink[3] + 1))


def texto_pixelado(texto, tamanho, escala, paleta=PALETA_MENU, raio=1):
    """Devolve uma imagem RGBA com o texto em pixel art já ampliada."""
    margem = raio + 2
    base = _mascara(texto, tamanho)
    tela = Image.new("L", (base.width + 2 * margem, base.height + 2 * margem + 1), 0)
    tela.paste(base, (margem, margem))
    contorno = tela.filter(ImageFilter.MaxFilter(2 * raio + 1))

    W, H = tela.size
    pm, pc = tela.load(), contorno.load()
    img = Image.new("RGBA", (W, H + 1), (0, 0, 0, 0))
    pi = img.load()

    linhas = [y for y in range(H) if any(pm[x, y] for x in range(W))]
    if not linhas:                        # nada desenhado: devolve imagem mínima
        return img.resize((img.width * escala, img.height * escala), Image.NEAREST)
    topo, fundo = min(linhas), max(linhas)
    altura = max(1, fundo - topo + 1)

    for y in range(H):
        for x in range(W):
            if pc[x, y]:
                pi[x, y + 1] = CONTORNO     # sombra
    for y in range(H):
        for x in range(W):
            if pc[x, y]:
                pi[x, y] = CONTORNO         # contorno
    for y in range(H):
        for x in range(W):
            if pm[x, y]:
                faixa = min(int((y - topo) / altura * len(paleta)), len(paleta) - 1)
                pi[x, y] = paleta[faixa] + (255,)

    return img.resize((img.width * escala, img.height * escala), Image.NEAREST)