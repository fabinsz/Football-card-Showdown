import pygame
import sys
import random
from EditorDeck import carregar_deck_usuario
from Classes.carta import Carta


pygame.init()
screen_width, screen_height = 1043, 755
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Fut Champions')
clock = pygame.time.Clock()

# Carrega e redimensiona a imagem de fundo
background_surface = pygame.image.load('Imagens/Jogo/fundo_game.jpg')
background_surface = pygame.transform.scale(background_surface, (screen_width, screen_height))

verso_image = pygame.image.load('Imagens/Cartas/Verso.png')
verso_image =  pygame.transform.scale(verso_image, (110, 150))

# Chame a função carregar_deck_usuario para obter as informações do deck
nomes_cartas = carregar_deck_usuario('deck_jogador_info.json')



# Chame a função carregar_deck_usuario para obter as informações do deck
nomes_cartas = carregar_deck_usuario('deck_jogador_info.json')

# Criar instâncias das cartas usando as informações do deck carregado
cartas_do_deck = []
cartas_na_mao = []

for nome_carta in nomes_cartas:
    caminho_imagem = f'imagens/Cartas/{nome_carta}.png'
    carta = Carta(nome_carta, 150, 590, "", caminho_imagem, 110, 150)
    cartas_do_deck.append(carta)

random.shuffle(cartas_do_deck)

# Distribua as primeiras 4 cartas na mão do jogador e remova do deck
cartas_na_mao = cartas_do_deck[:4]
cartas_no_deck = cartas_do_deck[4:]

# Defina a posição base X para as cartas na mão
posicao_base_x_mao = 300  # Ajuste conforme necessário
    
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Desenha a imagem de fundo
        screen.blit(background_surface, (0, 0))

    for carta in cartas_no_deck:
            screen.blit(carta.image, carta.rect.topleft)
            
    # Ajuste a posição X das cartas na mão do jogador
    for i, carta in enumerate(cartas_na_mao):
        carta.rect.x = posicao_base_x_mao + i * 120  # Ajuste conforme necessário
        carta.rect.y = 580  # Ajuste conforme necessário
        screen.blit(carta.image, (carta.rect.x, carta.rect.y))                                
    screen.blit(verso_image, (150, 590))
    
    
    pygame.display.update()
    clock.tick(60)

