import sys
import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1043, 755))
pygame.display.set_caption('Fut Champions')
clock = pygame.time.Clock()

# Fonte
main_font = pygame.font.Font('Fontes/Bahnschrift.ttf', 15)
input_font = pygame.font.Font('Fontes/Bahnschrift.ttf', 20)
title_font_bold = pygame.font.Font('Fontes/Karla.ttf', 25)
title_font_bold.set_bold(True)

# Cores
gray_color = (246, 245, 245)
black_color = (0, 0, 0)
brown_color = (73, 49, 49)
white_color = (255, 255, 255)

# Imagem da direita
background_surface = pygame.image.load('Imagens/Cadastro.jpg')

# Botão da seta
arrow = pygame.image.load('Imagens/Botão seta.png')
arrow = pygame.transform.scale(arrow, (60, 60))
arrow_rect = arrow.get_rect(topleft=(118, 560))
arrow_hovered = False

# Criar o objeto retângulo
rectangle = pygame.Surface((305, 755))
rectangle.fill(gray_color)

# Cria os objetos de textos
text1 = title_font_bold.render('Crie sua conta', True, black_color)
text2 = main_font.render('Nome de usuário:', True, black_color)
text3 = main_font.render('Senha:', True, black_color)
text4 = main_font.render('Confirmar senha:', True, black_color)
text5 = main_font.render('Já possui uma conta?', True, black_color)

# Função para criar botões
def create_button(text, font, text_color, button_color, btn_width, btn_height, position):
    btn_surface = pygame.Surface((btn_width, btn_height))
    btn_surface.fill(button_color)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(btn_width // 2, btn_height // 2))
    btn_surface.blit(text_surface, text_rect)

    button_rect = btn_surface.get_rect(center=position)
    return btn_surface, button_rect

# Cria o botão "fazer Login"
button_fazer_login, button_rect_fazer_login = create_button(
    'fazer Login', main_font, brown_color, gray_color,
    200, 20, (rectangle.get_width() // 2.1, 700)
)

# Caixas de preenchimento de dados
input_box_width = 236
input_box_height = 46
username_box = pygame.Rect(30, 210, input_box_width, input_box_height)
password_box = pygame.Rect(30, 310, input_box_width, input_box_height)
confirm_password_box = pygame.Rect(30, 410, input_box_width, input_box_height)

# Variáveis para armazenar o texto dos campos
username_text = ''
password_text = ''
confirm_password_text = ''

# Função para adicionar texto aos campos
def draw_text_in_box(surface, text, color, rect, font):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(rect.x + 5, rect.y + 5))
    if text_rect.width > rect.width - 10:
        text = text[:len(text)-1]
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(rect.x + 5, rect.y + 5))
    surface.blit(text_surface, text_rect)

while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect_fazer_login.collidepoint(event.pos):
                pygame.quit()
                login_script = os.path.join(os.path.dirname(__file__), "Login.py")
                os.system(f"python {login_script}")
                sys.exit()

            elif arrow_rect.collidepoint(event.pos):
                if username_text and password_text and confirm_password_text:
                    if password_text == confirm_password_text:
                        # Salvar dados do jogador em arquivo TXT
                        player_data = f"{username_text},{password_text}\n"  # Formato: nome de usuário, senha

                        with open('dados_jogadores.txt', 'a') as file:  # 'a' para adicionar ao arquivo
                            file.write(player_data)

                        print("Dados do jogador salvos com sucesso!")
                    else:
                        print("Senhas não coincidem!")
                else:
                    print("Preencha todos os campos!")

        # Captura a entrada do teclado para os campos de texto
        if event.type == pygame.KEYDOWN:
            if username_box.collidepoint(mouse_x, mouse_y):
                if event.key == pygame.K_BACKSPACE:
                    username_text = username_text[:-1]
                else:
                    username_text += event.unicode
            elif password_box.collidepoint(mouse_x, mouse_y):
                if event.key == pygame.K_BACKSPACE:
                    password_text = password_text[:-1]
                else:
                    password_text += event.unicode
            elif confirm_password_box.collidepoint(mouse_x, mouse_y):
                if event.key == pygame.K_BACKSPACE:
                    confirm_password_text = confirm_password_text[:-1]
                else:
                    confirm_password_text += event.unicode

    # Desenha a imagem de fundo
    screen.blit(background_surface, (100, -50))

    # Desenha o retângulo
    screen.blit(rectangle, (0, 0))

    # Posições de text1 no retângulo
    text_1 = text1.get_rect()
    text_1.topleft = (30, 100)

    # Posições de text2 no retângulo
    text_2 = text2.get_rect()
    text_2.topleft = (30, 180)

    # Posições de text3 no retângulo
    text_3 = text3.get_rect()
    text_3.topleft = (30, 280)
    
    # Posições de text4 no retângulo
    text_4 = text4.get_rect()
    text_4.topleft = (30, 380)
    
    # Posições de text5 no retângulo
    text_5 = text5.get_rect()
    text_5.topleft = (75, 660)

    # Desenha os textos na tela
    screen.blit(text1, text_1)
    screen.blit(text2, text_2)
    screen.blit(text3, text_3)
    screen.blit(text4, text_4)
    screen.blit(text5, text_5)
        
    # Desenha o botão "fazer Login"
    screen.blit(button_fazer_login, button_rect_fazer_login)
    
    # Verifica se o mouse está sobre o botão "fazer Login"
    if button_rect_fazer_login.collidepoint(mouse_x, mouse_y):
        underline_length = int(button_rect_fazer_login.width * 0.55)
        line_start = (button_rect_fazer_login.centerx - underline_length / 2, button_rect_fazer_login.bottom - 2)
        line_end = (button_rect_fazer_login.centerx + underline_length / 2, button_rect_fazer_login.bottom - 2)

        # Desenha o sublinhado
        pygame.draw.line(screen, brown_color, line_start, line_end, 2)

    # Desenha as caixas de preenchimento de dados
    pygame.draw.rect(screen, brown_color, username_box)
    pygame.draw.rect(screen, black_color, username_box, 2)
    pygame.draw.rect(screen, brown_color, password_box)
    pygame.draw.rect(screen, black_color, password_box, 2)
    pygame.draw.rect(screen, brown_color, confirm_password_box)
    pygame.draw.rect(screen, black_color, confirm_password_box, 2)

    # Desenha o botão seta
    screen.blit(arrow, arrow_rect.topleft)

    # Verifica se o mouse está sobre o botão seta
    arrow_hovered = arrow_rect.collidepoint(mouse_x, mouse_y)

    # Desenha o botão seta com borda diferente se o mouse estiver sobre ele
    if arrow_hovered:
        pygame.draw.rect(screen, white_color, arrow_rect, 2)
    else:
        pygame.draw.rect(screen, black_color, arrow_rect, 2)

    # Desenha o texto nos campos de entrada
    draw_text_in_box(screen, username_text, white_color, username_box, main_font)
    draw_text_in_box(screen, '*' * len(password_text), white_color, password_box, main_font)  # Para senha, exibe asteriscos
    draw_text_in_box(screen, '*' * len(confirm_password_text), white_color, confirm_password_box, main_font)  # Confirmar senha também exibe asteriscos

    pygame.display.update()
    clock.tick(60)
