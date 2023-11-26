import pygame

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Classe para representar uma carta
class Carta(pygame.sprite.Sprite):
    def __init__(self, nome, x, y, cor, descricao):
        super().__init__()
        self.nome = nome
        self.cor = cor  # Adicione a cor como um atributo
        self.descricao = descricao
        self.image = pygame.Surface((100, 150))
        self.atualizar_cor()  # Use o método para atualizar a cor
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.brilho = False
        self.cor_brilho = YELLOW  # Cor padrão para brilho amarelo
        self.em_slot = False  # Novo atributo para indicar se a carta está em um slot
        self.pos_inicial = (x, y)  # Posição inicial da carta
        self.sendo_arrastada = False  # Indica se a carta está sendo arrastada
        self.em_slot = False  # Indica se a carta está em um slot
        self.slot_rect = pygame.Rect(0, 0, 0, 0)  # Retângulo que representa o slot da carta

    def atualizar_cor(self):
        self.image.fill(self.cor)  # Atualiza a cor da imagem
    
    def brilhar(self):
        self.brilho = True
    
    def update(self):
        if self.brilho:
            # Altere a cor para a cor de brilho desejada
            pygame.draw.rect(self.image, self.cor_brilho,
            self.image.get_rect(), 3)  # 3 é a largura da borda
        else:
            self.image.fill(self.cor)  # Cor original
        
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

