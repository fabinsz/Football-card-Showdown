import pygame

class CartaAumentada(pygame.sprite.Sprite):
    def __init__(self, carta_original):
        super().__init__()

        # Crie uma cópia da imagem da carta original
        self.image = carta_original.image.copy()

        # Redimensione a imagem para o tamanho desejado usando smoothscale
        nova_largura = 220
        nova_altura = 300
        self.image = pygame.transform.smoothscale(self.image, (nova_largura, nova_altura))

        # Atualize o retângulo para a posição desejada na tela
        self.rect = self.image.get_rect()
        self.rect.topleft = (40, 20)  # Defina a posição inicial desejada

        # Mantenha uma referência à carta original
        self.carta_original = carta_original
        
        self.brilho = True
        
