import pygame
import os

nome_fonte = "BAHNSCHRIFT.TTF"
caminho_fonte = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Fontes", nome_fonte)

class DescricaoCarta(pygame.sprite.Sprite):
    def __init__(self, descricao, x, y, largura_max_por_linha=300):
        super().__init__()
        self.descricao = descricao
        self.largura_max_por_linha = largura_max_por_linha
        self.font = pygame.font.Font(caminho_fonte, 20)
        self.image = self.renderizar_descricao()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        

    def renderizar_descricao(self):
        descricao_quebrada = self.quebrar_descricao()
        texto_renderizado = []
        for linha in descricao_quebrada:
            linha_renderizada = self.font.render(linha, True, (0, 0, 0))
            texto_renderizado.append(linha_renderizada)
        
        # Combine as linhas renderizadas em uma única imagem
        altura_total = sum(linha_renderizada.get_height() for linha_renderizada in texto_renderizado)
        imagem_final = pygame.Surface((self.largura_max_por_linha, altura_total), pygame.SRCALPHA)
        altura_atual = 0
        for linha_renderizada in texto_renderizado:
            imagem_final.blit(linha_renderizada, (0, altura_atual))
            altura_atual += linha_renderizada.get_height()

        return imagem_final

    def quebrar_descricao(self, palavras_por_linha=5):
     palavras = self.descricao.split()
     linhas = []
     for i in range(0, len(palavras), palavras_por_linha):
        linha_atual = " ".join(palavras[i:i+palavras_por_linha])
        linhas.append(linha_atual)
     return linhas