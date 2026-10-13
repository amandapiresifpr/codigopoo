"""
Mede a altura do chão desenhado no fundo.png, do jeito que o jogo o mostra
(imagem esticada para 800 x 600).

Uso (na pasta do jogo):
    python medir_chao.py              # usa fundo.png
    python medir_chao.py outro.png

O número final é o valor de TOPO_CHAO: o y (contado a partir da BASE da
janela, como o Arcade conta) onde começa a grama do chão.
"""
import sys
from statistics import median

from PIL import Image

LARGURA = 800
ALTURA = 600


def eh_grama(cor):
    r, g, b = cor[:3]
    return g > r + 35 and g > b + 60 and r < 190


def medir(caminho):
    imagem = Image.open(caminho).convert("RGB").resize((LARGURA, ALTURA))
    pixels = imagem.load()

    topos = []
    # Só o miolo da tela (longe das árvores), de cima para baixo
    for x in range(200, 600, 5):
        for y in range(ALTURA // 2, ALTURA - 8):
            if all(eh_grama(pixels[x, y + k]) for k in range(8)):
                topos.append(ALTURA - y)   # linha da imagem -> y do jogo
                break
    return topos


if __name__ == "__main__":
    arquivo = sys.argv[1] if len(sys.argv) > 1 else "fundo.png"
    topos = medir(arquivo)
    if not topos:
        print("Não achei grama. Confira se o arquivo é o fundo do jogo.")
        sys.exit(1)

    print(f"Colunas medidas: {len(topos)}")
    print(f"Topo do chão: mínimo {min(topos)}, mediana {median(topos):.0f}, máximo {max(topos)}")
    print()
    print(f"==> use  TOPO_CHAO = {round(median(topos))}")