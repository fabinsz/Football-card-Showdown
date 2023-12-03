import sys
import pygame
import os

pygame.init()
screen_width, screen_height = 1043, 755
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Fut Champions')
clock = pygame.time.Clock()

# Fontes
main_font = pygame.font.Font('Fontes/Bahnschrift.ttf', 30)
main_font2 = pygame.font.Font('Fontes/Bahnschrift.ttf', 25)
main_font.set_bold(True)

# Cores
white_color = (255, 255, 255)
black_color = (0, 0, 0)
brown_color = (79, 45, 45)

# Carrega e redimensiona a imagem de fundo
background_surface = pygame.image.load('Imagens/campinho tatico.jpg')
background_surface = pygame.transform.scale(background_surface, (screen_width, screen_height))

# Cria os objeto de texto Stats
stats = main_font.render('STATS', True, black_color)

# Cria os objeto de texto central
victory = main_font2.render('Vitórias -------------------------000', True, white_color)
defeats = main_font2.render('Derrotas ------------------------000', True, white_color)
goals_scored = main_font2.render('Gols marcados ------------------000', True, white_color)
goals_conceded = main_font2.render('Gols sofridos --------------------000', True, white_color)
total_matches = main_font2.render('Total de partidas -----------------000', True, white_color)

# Criar o objeto retângulo superior
top_rectangle = pygame.Surface((1043, 64))
top_rectangle.fill(white_color)

# Adicionar borda preta ao retângulo superior
pygame.draw.rect(top_rectangle, black_color, top_rectangle.get_rect(), 1)

# Criar o objeto retângulo central
center_rectangle = pygame.Surface((488, 336))
center_rectangle.fill(brown_color)


# Criar um retângulo para a borda preta
border_rect = pygame.Surface((center_rectangle.get_width() + 6.5, center_rectangle.get_height() + 6.5))
border_rect.fill(black_color)
border_rect.blit(center_rectangle, (3.9, 3.9))

# Função para criar botão
def create_button(text, font, text_color, button_color, btn_width, btn_height, position):
    btn_surface = pygame.Surface((btn_width, btn_height))
    btn_surface.fill(button_color)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(btn_width // 2, btn_height // 2))
    btn_surface.blit(text_surface, text_rect)

    # Desenha o contorno preto no botão
    pygame.draw.rect(btn_surface, black_color, btn_surface.get_rect(), 2)

    button_rect = btn_surface.get_rect(center=position)
    return btn_surface, button_rect

# Calcula a posição central horizontal da tela
center_x = screen.get_width() // 2

# Cria o botão "Sair"
button_exit, button_rect_exit = create_button(
    'Voltar', main_font2, black_color, white_color,
    100, 50, (center_x, 650)
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect_exit.collidepoint(event.pos):
                pygame.quit()
                login_script = os.path.join(os.path.dirname(__file__), "Menu_inicial.py")
                os.system(f"python {login_script}")
                sys.exit()

    # Desenha a imagem de fundo
    screen.blit(background_surface, (0, 30))
    
    # Desenha o retângulo superior com a borda preta
    screen.blit(top_rectangle, (0, 15))

    # Desenha o retângulo central com a borda preta
    screen.blit(border_rect, (center_x - border_rect.get_width() // 2, 203))
    
    # Posições dos textos no retângulo central com espaçamento
    vitorias = victory.get_rect()
    vitorias.topleft = (290, 240)
    
    derrotas = defeats.get_rect()
    derrotas.topleft = (290, 300)
    
    gols_marcados = goals_scored.get_rect()
    gols_marcados.topleft = (290, 360)
    
    gols_sofridos = goals_conceded.get_rect()
    gols_sofridos.topleft = (290, 420)
    
    total_partidas = total_matches.get_rect()
    total_partidas.topleft = (290, 480)

    # Desenha os textos do retângulo central na tela
    screen.blit(victory, vitorias)
    screen.blit(defeats, derrotas)
    screen.blit(goals_scored, gols_marcados)
    screen.blit(goals_conceded, gols_sofridos)
    screen.blit(total_matches, total_partidas)

    # Posições de Stats no retângulo superior
    Stats_rect = stats.get_rect()
    Stats_rect.center = top_rectangle.get_rect().center
    Stats_rect.top += 15

    # Desenha o texto Stats na tela
    screen.blit(stats, Stats_rect)
    
    # Desenha o botão "Sair"
    screen.blit(button_exit, button_rect_exit)

    pygame.display.update()
    clock.tick(60)