import pygame

BLACK = (0, 0, 0)

# Classe para representar uma carta
class Carta(pygame.sprite.Sprite):
    def __init__(self, nome, x, y):
        super().__init__()
        self.nome = nome
        self.image = pygame.Surface((50, 75))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)