import pygame
import os

nome_fonte = "BAHNSCHRIFT.TTF"
caminho_fonte = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Fontes", nome_fonte)

class DescricaoCarta(pygame.sprite.Sprite):
    def __init__(self, descricao, x, y):
        super().__init__()
        self.descricao = descricao
        self.font = pygame.font.Font(caminho_fonte, 24)
        self.image = self.font.render(descricao, True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)