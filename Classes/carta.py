import pygame

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Classe para representar uma carta
class Carta(pygame.sprite.Sprite):
    def __init__(self, nome, x, y, descricao, image_path, largura, altura):
        super().__init__()
        self.nome = nome
        self.descricao = descricao
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(self.original_image, (largura, altura))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.brilho = False
        self.cor_brilho = YELLOW
        self.em_slot = False
        self.pos_inicial = (x, y)
        self.sendo_arrastada = False
        self.em_slot = False
        self.slot_rect = pygame.Rect(0, 0, 0, 0)

    def update(self):
        if self.brilho:
            # Crie uma nova imagem com o tamanho original
            self.image = pygame.transform.smoothscale(self.original_image, (self.rect.width, self.rect.height))
            # Desenhe o retângulo de brilho na nova imagem
            pygame.draw.rect(self.image, self.cor_brilho, self.image.get_rect(), 3)
        else:
            # Mantenha o tamanho original sem retângulo de brilho
            self.image = pygame.transform.smoothscale(self.original_image, (self.rect.width, self.rect.height))

        if self.em_slot:
            # Ajuste a posição para a do slot
            if isinstance(self.slot_rect, tuple):
                self.slot_rect = pygame.Rect(self.slot_rect)
                self.rect.topleft = self.slot_rect.topleft

        if self.sendo_arrastada:
            # Atualize a posição durante o arrasto
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.center = (mouse_x, mouse_y)

        if self.em_slot and not self.sendo_arrastada:
            if isinstance(self.slot_rect, tuple):
                self.slot_rect = pygame.Rect(self.slot_rect)