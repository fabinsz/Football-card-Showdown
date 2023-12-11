import pygame
import sys
import random
from EditorDeck import carregar_deck_usuario , criar_cartas_disponiveis , Deck
from Classes.carta import Carta
from Classes.Bot import escolher_carta_bot


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
verso_inimigo = verso_image

Slot_A = pygame.image.load('Imagens/Slot.png')
Slot_A = pygame.transform.scale(Slot_A, (150, 275))
Slot_B = Slot_A
Slot_C = Slot_A



# Criar um deck para o inimigo (bot)
deck_inimigo = Deck()
cartas_inimigo = criar_cartas_disponiveis()

# Adicione cartas aleatórias ao deck do inimigo (bot)
num_cartas_inimigo = 8  # Número desejado de cartas no deck do inimigo
indices_cartas_aleatorias = random.sample(range(len(cartas_inimigo)), num_cartas_inimigo)

for indice in indices_cartas_aleatorias:
    carta_aleatoria = cartas_inimigo[indice]
    deck_inimigo.adicionar_carta(carta_aleatoria)

# Criar uma lista para armazenar as cartas na mão do inimigo
cartas_na_mao_inimigo = []

# Adicionar 3 cartas aleatórias do deck do inimigo à mão do inimigo
indices_cartas_mao_aleatorias = random.sample(range(len(deck_inimigo.cartas)), 3)

for indice in indices_cartas_mao_aleatorias:
    carta_mao_aleatoria = deck_inimigo.cartas[indice]
    cartas_na_mao_inimigo.append(carta_mao_aleatoria)

# Remover as cartas da mão do inimigo do deck do inimigo
deck_inimigo.cartas = [carta for carta in deck_inimigo.cartas if carta not in cartas_na_mao_inimigo]


# Atualizar as cartas na mão do inimigo
for carta in cartas_na_mao_inimigo:
    carta.update()

# Chame a função carregar_deck_usuario para obter as informações do deck
nomes_cartas = carregar_deck_usuario('deck_jogador_info.json')

# Criar instâncias das cartas usando as informações do deck carregado
cartas_do_deck = []
cartas_na_mao = []

cartas_slot_c = []
cartas_slot_a = []
cartas_slot_b = []

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
posicao_base_x_mao2 = 250

posicao_base_x_deck_inimigo = 100  # Ajuste conforme necessário
posicao_base_y_deck_inimigo = 10  # Ajuste conforme necessário    


turno_jogador = True
tempo_espera_bot = 0
tempo_espera_bot_fixo = 3000
contador_turnos = 0
contador_turnos2 = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
           if turno_jogador: 
            
            
            for carta in cartas_na_mao:
                if carta.rect.collidepoint(event.pos):
                    # Verifica se o nome da carta está na lista permitida
                    if carta.nome in ['Avanço 5', 'Avanço 10', 'Avanço 15', 'Meio campo', 'Torcida', 'Lesão']:
                        # Adiciona a carta clicada ao deck do jogador
                        cartas_slot_c.append(carta)
                        # Remove a carta da mão do jogador
                        cartas_na_mao.remove(carta)
                        # Define uma nova posição para a carta clicada
                        nova_posicao_x = 850  # Defina a nova posição X conforme necessário
                        nova_posicao_y = 70  # Defina a nova posição Y conforme necessário
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)
                        contador_turnos2 += 1
                        
                    elif carta.nome in ['Chute livre', 'Penalti', 'Gol de ouro']:
                        # Adiciona a carta clicada ao deck do jogador
                        cartas_slot_a.append(carta)
                        # Remove a carta da mão do jogador
                        cartas_na_mao.remove(carta)
                        # Define uma nova posição para a carta clicada
                        nova_posicao_x = 280  # Defina a nova posição X conforme necessário
                        nova_posicao_y = 217 # Defina a nova posição Y conforme necessário
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)  
                        contador_turnos2 += 1
                        
                    
                    elif carta.nome in ['Goleiro', 'Pressão']:
                        # Adiciona a carta clicada ao deck do jogador
                        cartas_slot_b.append(carta)
                        # Remove a carta da mão do jogador
                        cartas_na_mao.remove(carta)
                        # Define uma nova posição para a carta clicada
                        nova_posicao_x = 600  # Defina a nova posição X conforme necessário
                        nova_posicao_y = 217 # Defina a nova posição Y conforme necessário
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y) 
                        contador_turnos2 += 1
                    
                    turno_jogador = False
                    

        if not turno_jogador and pygame.time.get_ticks() - tempo_espera_bot>= tempo_espera_bot_fixo:
                        carta_bot = escolher_carta_bot(cartas_na_mao_inimigo)  
                        if carta_bot:
                            if carta_bot.nome in ['Chute livre', 'Penalti', 'Gol de ouro']:
                                # Adiciona a carta do bot ao deck do jogador
                                cartas_slot_b.append(carta_bot)
                                # Remove a carta da mão do bot
                                cartas_na_mao_inimigo.remove(carta_bot)
                                # Define uma nova posição para a carta do bot
                                nova_posicao_x_bot = 280  # Defina a nova posição X conforme necessário
                                nova_posicao_y_bot = 217  # Defina a nova posição Y conforme necessário
                                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                                contador_turnos += 1 
                                
                                

                            elif carta_bot.nome in ['Avanço 5', 'Avanço 10', 'Avanço 15', 'Meio campo', 'Torcida', 'Lesão']:
                                # Adiciona a carta do bot ao deck do jogador
                                cartas_slot_c.append(carta_bot)
                                # Remove a carta da mão do bot
                                cartas_na_mao_inimigo.remove(carta_bot)
                                # Define uma nova posição para a carta do bot
                                nova_posicao_x_bot = 850  # Defina a nova posição X conforme necessário
                                nova_posicao_y_bot = 70  # Defina a nova posição Y conforme necessário
                                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                                contador_turnos += 1 
                                
                                

                            elif carta_bot.nome in ['Goleiro', 'Pressão']:
                                # Adiciona a carta do bot ao deck do jogador
                                cartas_slot_a.append(carta_bot)
                                # Remove a carta da mão do bot
                                cartas_na_mao_inimigo.remove(carta_bot)
                                # Define uma nova posição para a carta do bot
                                nova_posicao_x_bot = 600  # Defina a nova posição X conforme necessário
                                nova_posicao_y_bot = 217  # Defina a nova posição Y conforme necessário
                                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                                contador_turnos += 1 
                            
                            turno_jogador = True
                            tempo_espera_bot = pygame.time.get_ticks()  # Atualiza o tempo de espera do bot
                            
        
    # Lógica de compra de cartas apenas no turno do jogador
    if contador_turnos == 1 and turno_jogador:
        if len(cartas_no_deck)  :
            # Adiciona uma carta do deck à mão do jogador
            carta_comprada = cartas_no_deck.pop(0)
            cartas_na_mao.append(carta_comprada)
               

    
    # Lógica de compra de cartas apenas no turno do jogador
    if contador_turnos2 >= 1 and not turno_jogador:
     if len(deck_inimigo.cartas) > 0:
        # Adiciona uma carta do deck à mão do bot
        carta_comprada_bot = deck_inimigo.cartas.pop(0)
        cartas_na_mao_inimigo.append(carta_comprada_bot)      


    
    contador_turnos = 0
    contador_turnos2 = 0
     
    # Desenha a imagem de fundo
    screen.blit(background_surface, (0, 0))

    for carta in cartas_no_deck:
        screen.blit(carta.image, carta.rect.topleft)
        screen.blit(verso_image, carta.rect.topleft)
        
    for carta in cartas_slot_c:
        screen.blit(carta.image, carta.rect.topleft) 
    
    for carta in cartas_slot_a:
        screen.blit(carta.image, carta.rect.topleft)
        
    for carta in cartas_slot_b:
        screen.blit(carta.image, carta.rect.topleft)             

    # Ajusta a posição X das cartas na mão do jogador
    for i, carta in enumerate(cartas_na_mao):
        carta.rect.x = posicao_base_x_mao + i * 120  # Ajuste conforme necessário
        carta.rect.y = 580  # Ajuste conforme necessário
        screen.blit(carta.image, (carta.rect.x, carta.rect.y))

    # Desenha as cartas na mão do inimigo na tela
    for i, carta in enumerate(cartas_na_mao_inimigo):
        x = posicao_base_x_mao2 + i * 120  # Ajuste conforme necessário
        y = 15  # Ajuste conforme necessário
        screen.blit(carta.image, (x, y))
        screen.blit(verso_inimigo, (x, y))

    for i, carta in enumerate(deck_inimigo.cartas):
        x = posicao_base_x_deck_inimigo  # Ajuste conforme necessário
        y = posicao_base_y_deck_inimigo
        screen.blit(carta.image, (x, y))
        screen.blit(verso_inimigo, (100, 10))

    screen.blit(Slot_A, (270, 200))
    screen.blit(Slot_B, (590, 200))
    screen.blit(Slot_C, (840, 53))
    
        
    pygame.display.update()
    clock.tick(60)

