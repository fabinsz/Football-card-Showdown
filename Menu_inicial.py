import sys
import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1043, 755))
pygame.display.set_caption('Fut Champions')
clock = pygame.time.Clock()

# Imagem da direita
background_surface = pygame.image.load('Imagens/Menu principal.jpg')

# Carrega as fontes
gamename_font = pygame.font.Font('Fontes/FRAHV.TTF', 35)
button_font = pygame.font.Font('Fontes/Bahnschrift.ttf', 24)

# Cores
brown_color = (73, 49, 49)
yellow_color = (248, 245, 28)
red_color = (251, 7, 7)
white_color = (255, 255, 255)
black_color = (0, 0, 0)

# Criar o objeto retângulo
rectangle = pygame.Surface((305, 755))
rectangle.fill(brown_color)

# Cria os objetos de texto para o gamename
text_fut = gamename_font.render('FUT', True, yellow_color)
text_champions = gamename_font.render('CHAMPIONS', True, red_color)

# Função para criar botões
def create_button(text, font, text_color, button_color, btn_width, btn_height, position):
    btn_surface = pygame.Surface((btn_width, btn_height))
    btn_surface.fill(button_color)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(btn_width // 2, btn_height // 2))
    btn_surface.blit(text_surface, text_rect)

    # Adiciona borda preta
    pygame.draw.rect(btn_surface, black_color, btn_surface.get_rect(), 2)

    button_rect = btn_surface.get_rect(center=position)
    return btn_surface, button_rect

# Cria os botões
btn_width = 232
btn_height = 41
button_jogar, button_rect1 = create_button(
    'Jogar', button_font, black_color, white_color,
    btn_width, btn_height, (rectangle.get_width() // 2, 315)
)
button_stats, button_rect2 = create_button(
    'Stats', button_font, black_color, white_color,
    btn_width, btn_height, (rectangle.get_width() // 2, button_rect1.bottom + 50)
)
button_editardeck, button_rect3 = create_button(
    'Editar Deck', button_font, black_color, white_color,
    btn_width, btn_height, (rectangle.get_width() // 2, button_rect2.bottom + 50)
)
button_sair, button_rect4 = create_button(
    'Sair', button_font, black_color, white_color,
    btn_width, btn_height, (rectangle.get_width() // 2, button_rect3.bottom + 50)
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #Estrutura para clicar em "Sair"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect4.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                sys.exit()
                
        #Estrutura para clicar em "Editar Deck"
            elif button_rect3.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                editordeck_script = os.path.join(os.path.dirname(__file__), "EditorDeck.py")
                os.system(f"python {editordeck_script}")
                sys.exit()
        
        #Estrutura para clicar em "Stats"
            elif button_rect2.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                Stats_script = os.path.join(os.path.dirname(__file__), "Stats.py")
                os.system(f"python {Stats_script}")
                sys.exit()      
        
        #Estrutura para clicar em "Jogar"
            elif button_rect1.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                Stats_script = os.path.join(os.path.dirname(__file__), "Game.py")
                os.system(f"python {Stats_script}")
                sys.exit()           
    
    # Obtém as coordenadas do mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Verifica se o mouse está sobre cada botão e muda a cor da borda
    button_rect1_color = black_color if not button_rect1.collidepoint(mouse_x, mouse_y) else red_color
    button_rect2_color = black_color if not button_rect2.collidepoint(mouse_x, mouse_y) else red_color
    button_rect3_color = black_color if not button_rect3.collidepoint(mouse_x, mouse_y) else red_color
    button_rect4_color = black_color if not button_rect4.collidepoint(mouse_x, mouse_y) else red_color

    # Desenha a imagem de fundo
    screen.blit(background_surface, (140, 0))

    # Desenha o retângulo marrom
    screen.blit(rectangle, (0, 0))

    # Posições do gamename no retângulo
    text_rect_fut = text_fut.get_rect()
    text_rect_fut.topleft = (30, 12)
    text_rect_champions = text_champions.get_rect()
    text_rect_champions.topleft = (30, text_rect_fut.bottom + 5)  # Posiciona abaixo de "Fut"

    # Desenha os textos gamename na tela
    screen.blit(text_fut, text_rect_fut)
    screen.blit(text_champions, text_rect_champions)

    # Desenha os botões na tela
    screen.blit(button_jogar, button_rect1)
    pygame.draw.rect(screen, button_rect1_color, button_rect1, 2)
    
    screen.blit(button_stats, button_rect2)
    pygame.draw.rect(screen, button_rect2_color, button_rect2, 2)
    
    screen.blit(button_editardeck, button_rect3)
    pygame.draw.rect(screen, button_rect3_color, button_rect3, 2)
    
    screen.blit(button_sair, button_rect4)
    pygame.draw.rect(screen, button_rect4_color, button_rect4, 2)

    pygame.display.update()
    clock.tick(60)