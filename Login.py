import sys
import pygame
import os
from EditorDeck import carregar_deck_usuario

pygame.init()
screen = pygame.display.set_mode((1043, 755))
pygame.display.set_caption('Fut Champions')
clock = pygame.time.Clock()

# Fonte
main_font = pygame.font.Font('Fontes/Bahnschrift.ttf', 15)
other_font = pygame.font.Font('Fontes/Bahnschrift.ttf', 15)
title_font_bold = pygame.font.Font('Fontes/Karla.ttf', 25)
title_font_bold.set_bold(True)

# Cores
gray_color = (246, 245, 245)
black_color = (0, 0, 0)
brown_color = (73, 49, 49)
white_color = (255, 255, 255)
highlight_color = (150, 150, 150)  # Cor para destacar o botão da seta

# Imagem da direita
background_surface = pygame.image.load('Imagens/Login.jpg')

# Botão da seta
arrow = pygame.image.load('Imagens/Botão seta.png')
arrow = pygame.transform.scale(arrow, (60, 60))
arrow_rect = arrow.get_rect(topleft=(118, 560))
arrow_hover = False  # Flag para verificar se o mouse está sobre o botão da seta

# Criar o objeto retângulo
rectangle = pygame.Surface((305, 755))
rectangle.fill(gray_color)

# Cria os objetos de textos
text1 = title_font_bold.render('Insira sua conta', True, black_color)
text2 = main_font.render('Nome de usuário:', True, black_color)
text3 = main_font.render('Senha:', True, black_color)

# Definindo uma nova fonte para a senha
password_font = pygame.font.Font('Fontes/Bahnschrift.ttf', 18)

# Renderiza o texto 'Senha' com a nova fonte
text3 = password_font.render('Senha:', True, black_color)

# Posições de text3 no retângulo (centralizando um pouco mais)
text_3 = text3.get_rect()
text_3.topleft = (30, 370)

# Variáveis para armazenar o texto dos campos de entrada
username_text = ''
password_text = ''

# Definir cores para texto dentro dos campos
text_color = white_color  # Alteração para cor branca

# Variáveis para controlar o cursor piscante
cursor_timer = 0
show_cursor = True
CURSOR_BLINK_MS = 500  # Define a frequência de piscar do cursor em milissegundos

# Função para criar botões
def create_button(text, font, text_color, button_color, btn_width, btn_height, position):
    btn_surface = pygame.Surface((btn_width, btn_height))
    btn_surface.fill(button_color)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(btn_width // 2, btn_height // 2))
    btn_surface.blit(text_surface, text_rect)

    button_rect = btn_surface.get_rect(center=position)
    return btn_surface, button_rect

# Função para realizar o login verificando o arquivo de dados
def fazer_login(username, password):
    with open('dados_jogadores.txt', 'r') as file:
        for line in file:
            user, pwd = line.strip().split(',')
            if user == username and pwd == password:
                return True
    return False


# Cria o botão "Crie sua conta"
button_criar_conta, button_rect_criar_conta = create_button(
    'Crie sua conta', main_font, black_color, gray_color,
    200, 20, (rectangle.get_width() // 3.5, 700)
)

# Caixas de preenchimento de dados
input_box_width = 236
input_box_height = 46
username_box = pygame.Rect(30, 280, input_box_width, input_box_height)
password_box = pygame.Rect(30, 390, input_box_width, input_box_height)

login_sucesso = False

while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect_criar_conta.collidepoint(event.pos):
                pygame.quit()
                cadastro_script = os.path.join(os.path.dirname(__file__), "Cadastro.py")
                os.system(f"python {cadastro_script}")
                sys.exit()
            elif arrow_rect.collidepoint(event.pos):  # Verifica o clique no botão da seta
                if fazer_login(username_text, password_text):  # Verifica o login ao clicar na seta
                    print("Login bem-sucedido!")
                    login_sucesso = True
                else:
                    print("Usuário ou senha incorretos.")
                    incorrect_text = main_font.render('Usuário ou senha incorretos.', True, (255, 0, 0))  # Cor vermelha

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if username_box.collidepoint(mouse_x, mouse_y):
                    username_text = username_text[:-1]
                elif password_box.collidepoint(mouse_x, mouse_y):
                    password_text = password_text[:-1]
            else:
                if username_box.collidepoint(mouse_x, mouse_y) and len(username_text) < 31:  # Limita a 31 caracteres
                    username_text += event.unicode
                elif password_box.collidepoint(mouse_x, mouse_y) and len(password_text) < 31:  # Limita a 31 caracteres
                    password_text += event.unicode

    # Renderiza o texto nos campos de entrada com a cor branca
    username_surface = other_font.render(username_text, True, text_color)
    password_surface = other_font.render('*' * len(password_text), True, text_color)

    # Desenha a imagem de fundo
    screen.blit(background_surface, (100, 0))

    # Desenha o retângulo
    screen.blit(rectangle, (0, 0))

    # Posições de text1 no retângulo
    text_1 = text1.get_rect()
    text_1.topleft = (30, 130)

    # Posições de text2 no retângulo
    text_2 = text2.get_rect()
    text_2.topleft = (30, 250)

    # Desenha os textos na tela
    screen.blit(text1, text_1)
    screen.blit(text2, text_2)
    screen.blit(text3, text_3)
    
    # Desenha o botão "Crie sua conta"
    screen.blit(button_criar_conta, button_rect_criar_conta)
    
    # Verifica se o mouse está sobre o botão "fazer Login"
    if button_rect_criar_conta.collidepoint(mouse_x, mouse_y):
        underline_length = int(button_rect_criar_conta.width * 0.7)
        line_start = (button_rect_criar_conta.centerx - underline_length / 2, button_rect_criar_conta.bottom - 2)
        line_end = (button_rect_criar_conta.centerx + underline_length / 2, button_rect_criar_conta.bottom - 2)

        # Desenha o sublinhado
        pygame.draw.line(screen, brown_color, line_start, line_end, 2)

    # Desenha as caixas de preenchimento de dados
    pygame.draw.rect(screen, brown_color, username_box)
    pygame.draw.rect(screen, black_color, username_box, 2)
    pygame.draw.rect(screen, brown_color, password_box)
    pygame.draw.rect(screen, black_color, password_box, 2)

    # Desenha o texto nos campos de entrada com a cor branca
    screen.blit(username_surface, (username_box.x + 5, username_box.y + 15))  # Ajuste na posição de renderização
    screen.blit(password_surface, (password_box.x + 5, password_box.y + 15))  # Ajuste na posição de renderização

    # Verifica se o usuário ou senha estão incorretos para exibir a mensagem em vermelho
    if 'incorrect_text' in locals():
        screen.blit(incorrect_text, (password_box.x, password_box.y + password_box.height + 5))  # Ajuste na posição

    # Lógica para controlar o cursor piscante
    cursor_timer += clock.get_time()
    if cursor_timer >= CURSOR_BLINK_MS:
        show_cursor = not show_cursor
        cursor_timer = 0

    # Desenha o cursor piscante no campo de digitação ativo
    if show_cursor:
        if username_box.collidepoint(mouse_x, mouse_y):
            cursor_x = username_surface.get_width() + username_box.x + 5
            pygame.draw.line(screen, white_color, (cursor_x, username_box.y + 10),
                             (cursor_x, username_box.y + username_box.height - 10), 2)
        elif password_box.collidepoint(mouse_x, mouse_y):
            cursor_x = password_surface.get_width() + password_box.x + 5
            pygame.draw.line(screen, white_color, (cursor_x, password_box.y + 10),
                             (cursor_x, password_box.y + password_box.height - 10), 2)

    # Verifica se o mouse está sobre o botão da seta
    if arrow_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, highlight_color, arrow_rect, 3)  # Muda a cor da borda
        arrow_hover = True
    else:
        pygame.draw.rect(screen, black_color, arrow_rect, 3)  # Volta a cor original da borda
        arrow_hover = False

    # Desenha o botão seta
    screen.blit(arrow, arrow_rect.topleft)

    if login_sucesso == True:
        pygame.quit()
        menu_script = os.path.join(os.path.dirname(__file__), "Menu_inicial.py")
        os.system(f"python {menu_script}")
        sys.exit()

    pygame.display.update()
    clock.tick(60)
