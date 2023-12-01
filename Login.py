import sys
import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1043, 755))
pygame.display.set_caption('Fut Champions')
clock = pygame.time.Clock()

# Fonte
main_font = pygame.font.Font('Fontes/Bahnschrift.ttf', 20)
other_font = pygame.font.Font('Fontes/Bahnschrift.ttf', 15)
title_font_bold = pygame.font.Font('Fontes/Karla.ttf', 30)
title_font_bold.set_bold(True)

# Cores
gray_color = (246, 245, 245)
black_color = (0, 0, 0)
brown_color = (73, 49, 49)
white_color = (255, 255, 255)

# Imagem da direita
background_surface = pygame.image.load('Imagens/Login.jpeg')

# Botão da seta
arrow = pygame.image.load('Imagens/Botão seta.png')
arrow = pygame.transform.scale(arrow, (60, 60))
arrow_rect = arrow.get_rect(topleft=(118, 540))

# Criar o objeto retângulo
rectangle = pygame.Surface((305, 755))
rectangle.fill(gray_color)

# Cria os objetos de textos
text1 = title_font_bold.render('Insira sua conta', True, black_color)
text2 = main_font.render('Nome de usuário:', True, black_color)
text3 = main_font.render('Senha:', True, black_color)

# Função para criar botões
def create_button(text, font, text_color, button_color, btn_width, btn_height, position):
    btn_surface = pygame.Surface((btn_width, btn_height))
    btn_surface.fill(button_color)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(btn_width // 2, btn_height // 2))
    btn_surface.blit(text_surface, text_rect)

    button_rect = btn_surface.get_rect(center=position)
    return btn_surface, button_rect

# Cria o botão "Crie sua conta"
button_criar_conta, button_rect_criar_conta = create_button(
    'Crie sua conta', main_font, black_color, white_color,
    200, 20, (rectangle.get_width() // 3.5, 700)
)

# Caixas de preenchimento de dados
input_box_width = 236
input_box_height = 46
username_box = pygame.Rect(30, 280, input_box_width, input_box_height)
password_box = pygame.Rect(30, 420, input_box_width, input_box_height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect_criar_conta.collidepoint(event.pos):
                pygame.quit()
                cadastro_script = os.path.join(os.path.dirname(__file__), "Cadastro.py")
                os.system(f"python {cadastro_script}")
                sys.exit()

    # Desenha a imagem de fundo
    screen.blit(background_surface, (300, 0))

    # Desenha o retângulo
    screen.blit(rectangle, (0, 0))

    # Posições de text1 no retângulo
    text_1 = text1.get_rect()
    text_1.topleft = (30, 130)

    # Posições de text2 no retângulo
    text_2 = text2.get_rect()
    text_2.topleft = (30, 240)

    # Posições de text3 no retângulo
    text_3 = text3.get_rect()
    text_3.topleft = (30, 380)

    # Desenha os textos na tela
    screen.blit(text1, text_1)
    screen.blit(text2, text_2)
    screen.blit(text3, text_3)
    
    # Desenha o botão "Crie sua conta"
    screen.blit(button_criar_conta, button_rect_criar_conta)

    # Desenha as caixas de preenchimento de dados
    pygame.draw.rect(screen, brown_color, username_box)
    pygame.draw.rect(screen, black_color, username_box, 2)
    pygame.draw.rect(screen, brown_color, password_box)
    pygame.draw.rect(screen, black_color, password_box, 2)

    # Desenha o botão seta
    screen.blit(arrow, arrow_rect.topleft)

    pygame.display.update()
    clock.tick(60)