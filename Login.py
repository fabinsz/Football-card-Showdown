import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((1043, 755))
pygame.display.set_caption('Fut Champions')
clock = pygame.time.Clock()

# Fonte
main_font = pygame.font.Font('Fontes/Karla.ttf', 20)
other_font = pygame.font.Font('Fontes/Karla.ttf', 15)
title_font_bold = pygame.font.Font('Fontes/Karla.ttf', 30)
title_font_bold.set_bold(True)

# Cores
gray_color = (246, 245, 245)
black_color = (0, 0, 0)
brown_color = (73, 49, 49)
white_color = (255, 255, 255)

# Imagem da direita
background_surface = pygame.image.load('Imagens/Login.jpeg')

# Imagem da seta
arrow = pygame.image.load('Imagens/Seta.png')

# Criar o objeto retângulo
rectangle = pygame.Surface((305, 755))
rectangle.fill(gray_color)

# Cria os objetos de textos
text1 = title_font_bold.render('Insira sua conta', True, black_color)
text2 = main_font.render('Nome de usuário:', True, black_color)
text3 = main_font.render('Senha:', True, black_color)
text4 = other_font.render('Crie sua conta', True, black_color)

# Caixas de preenchimento de dados
input_box_width = 236
input_box_height = 46
username_box = pygame.Rect(30, 280, input_box_width, input_box_height)
password_box = pygame.Rect(30, 420, input_box_width, input_box_height)

# Adiciona o botão 1
button_width1 = 66
button_height1 = 66
button1 = pygame.Rect(110, 530, button_width1, button_height1)

# Adiciona o botão 2
button_width2 = 60
button_height2 = 60
button2 = pygame.Rect(113, 533, button_width2, button_height2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Desenha a imagem de fundo
    screen.blit(background_surface, (300, 0))
    
    # Resize the arrow image to 60x60
    arrow = pygame.transform.scale(arrow, (60, 60))
    
    # Desenha a seta
    screen.blit(arrow, (0, 0))

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

    # Posições de text4 no retângulo
    text_4 = text4.get_rect()
    text_4.topleft = (20, 700)

    # Desenha os textos na tela
    screen.blit(text1, text_1)
    screen.blit(text2, text_2)
    screen.blit(text3, text_3)
    screen.blit(text4, text_4)

    # Desenha as caixas de preenchimento de dados
    pygame.draw.rect(screen, brown_color, username_box)
    pygame.draw.rect(screen, black_color, username_box, 2)
    pygame.draw.rect(screen, brown_color, password_box)
    pygame.draw.rect(screen, black_color, password_box, 2)

    # Desenha o botão 1
    pygame.draw.rect(screen, black_color, button1, border_radius=10)

    # Desenha o botão 2
    pygame.draw.rect(screen, white_color, button2, border_radius=9)

    pygame.display.update()
    clock.tick(60)