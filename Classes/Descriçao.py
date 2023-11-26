import pygame

class DescricaoCarta(pygame.sprite.Sprite):
    def __init__(self, descricao, x, y):
        super().__init__()
        self.descricao = descricao
        self.font = pygame.font.Font(None, 24)
        self.image = self.font.render(descricao, True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)