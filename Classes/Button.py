import pygame


WIDTH, HEIGHT = 1043, 755
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Button:
    def __init__(self):
        self.rect = pygame.Rect(40, 460, 232, 41)
        self.normal_color = (73, 49, 49)
        self.hover_color = (10, 16, 28)
        self.color = self.normal_color
        self.text_color = (255, 255, 255)
        self.text_size = 30
        self.text = "Salvar/Voltar"
        self.clicked = False

    def render(self):
        mouse_pos = pygame.mouse.get_pos()
        is_mouse_collision = self.rect.collidepoint(mouse_pos)
        self.color = self.hover_color if is_mouse_collision else self.normal_color

        font = pygame.font.Font(None, self.text_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.clicked = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos) and self.clicked:
                self.clicked = False
                return True  # Indica que o botão foi clicado

        return False  # O botão não foi clicado
