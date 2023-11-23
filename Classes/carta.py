import pygame

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Classe para representar uma carta
class Carta(pygame.sprite.Sprite):
    def __init__(self, nome, x, y):
        super().__init__()
        self.nome = nome
        self.image = pygame.Surface((100, 150))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.brilho = False
        self.cor_brilho = (YELLOW) # Cor padrão para brilho amarelo
    def brilhar(self):
        self.brilho = True
    def update(self):
        if self.brilho:
            # Altere a cor para a cor de brilho desejada
            pygame.draw.rect(self.image, self.cor_brilho,
            self.image.get_rect(), 3)  # 3 é a largura da borda
        else:
            self.image.fill(BLACK)  # Cor original

