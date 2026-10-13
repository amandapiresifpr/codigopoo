"""
Gera os PNGs pixelados (vermelho e amarelo) do jogo Moranguinho.
Uso:  python gerar_titulos.py     (precisa do Pillow: pip install pillow)
"""
from PIL import Image

from texto_pixel import *

SOMBRA = CONTORNO


MORANGO = [
    "....GG.GG...",
    "...GGGGGGG..",
    "....GGGGG...",
    "..RRRGGGRRR.",
    ".RRRRRRRRRRR",
    ".RWRRRYRRYRR",
    ".RWRYRRRRRRR",
    ".RRRRRRYRRRR",
    "..RRYRRRRYR.",
    "..RRRRRYRRR.",
    "...RRYRRRR..",
    "....RRRRR...",
    ".....RRR....",
]
CORES_MORANGO = {
    "R": (235, 30, 35, 255), "G": (40, 170, 70, 255),
    "Y": (255, 215, 60, 255), "W": (255, 150, 150, 255),
}


def morango_pixelado(escala):
    h, w = len(MORANGO), len(MORANGO[0])
    img = Image.new("RGBA", (w + 2, h + 2), (0, 0, 0, 0))
    pi = img.load()
    for y, linha in enumerate(MORANGO):
        for x, c in enumerate(linha):
            if c in CORES_MORANGO:
                pi[x + 1, y + 1] = CORES_MORANGO[c]
    # contorno escuro
    saida = img.copy()
    po = saida.load()
    for y in range(img.height):
        for x in range(img.width):
            if pi[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < img.width and 0 <= ny < img.height and pi[nx, ny][3]:
                        po[x, y] = CONTORNO
                        break
    return saida.resize((saida.width * escala, saida.height * escala), Image.NEAREST)


def salvar(img, nome):
    img.save(nome)
    print(f"{nome}: {img.size[0]} x {img.size[1]} px")


def titulo_principal():
    titulo = texto_pixelado("MORANGUINHO", 16, 4, PALETA_TITULO, raio=1)
    sub = texto_pixelado("em busca dos morangos perdidos", 10, 3, PALETA_AMARELA, raio=1)
    m = morango_pixelado(4)

    larg = max(titulo.width, sub.width) + 2 * (m.width + 10)
    alt = titulo.height + sub.height + 6
    tela = Image.new("RGBA", (larg, alt), (0, 0, 0, 0))
    x_t = (larg - titulo.width) // 2
    tela.alpha_composite(titulo, (x_t, 0))
    tela.alpha_composite(sub, ((larg - sub.width) // 2, titulo.height + 6))
    y_m = (titulo.height - m.height) // 2
    tela.alpha_composite(m, (0, y_m))
    tela.alpha_composite(m, (larg - m.width, y_m))
    return tela


if __name__ == "__main__":
    salvar(titulo_principal(), "titulo.png")

    # Opções do menu
    menu = {
        "menu_jogar.png": "[J] Jogar",
        "menu_instrucoes.png": "[I] Instruções",
        "menu_sobre.png": "[S] Sobre o Jogo",
        "menu_ranking.png": "[R] Ranking",
        "menu_sair.png": "[ESC] Sair",
    }
    for arquivo, texto in menu.items():
        salvar(texto_pixelado(texto, 12, 3, PALETA_MENU, raio=1), arquivo)

    # Títulos da tela de fim de jogo
    salvar(texto_pixelado("FIM DE JOGO!", 18, 4, PALETA_DERROTA), "fim_derrota.png")
    salvar(texto_pixelado("Parabéns! Você terminou o jogo!", 12, 3, PALETA_MENU),
           "fim_vitoria.png")
    salvar(texto_pixelado("PONTUAÇÃO MÁXIMA!", 14, 4, PALETA_OURO), "fim_perfeito.png")