import pygame

class CartaAumentada(pygame.sprite.Sprite):
    def __init__(self, carta_original):
        super().__init__()

        # Crie uma cópia da imagem da carta original
        self.image = carta_original.image.copy()

        # Redimensione a imagem para o tamanho desejado
        self.image = pygame.transform.scale(self.image, (200, 300))

        # Atualize o retângulo para a posição desejada na tela
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, 20)  # Defina a posição inicial desejada

        # Mantenha uma referência à carta original
        self.carta_original = carta_original