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

mensage_font = pygame.font.Font('Fontes/FRAHV.TTF', 24)
mensagem_turno = mensage_font.render('É a sua vez!', True, (255, 255, 255))

# Carrega e redimensiona a imagem de fundo
background_surface = pygame.image.load('Imagens/Jogo/fundo_game.jpg')
background_surface = pygame.transform.scale(background_surface, (screen_width, screen_height))

Bola = pygame.image.load('Imagens/Jogo/bola.png')
Bola = pygame.transform.scale(Bola, (40, 40))
 

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
indices_cartas_mao_aleatorias = random.sample(range(len(deck_inimigo.cartas)), 4)

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

posicao_bola = 480
limite_minimo = 130
limite_maximo = 830

def arredondar_percentual(valor):
    if valor % 10 >= 3 and valor % 10 <= 7:
        return (valor // 10) * 10 + 5
    else:
        return (valor // 10) * 10


                
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
                    if carta.nome in ['Avanço 5']:
                        cartas_slot_c.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 850  
                        nova_posicao_y = 70  
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)
                        nova_posicao = posicao_bola + 48
                        posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao))
                        
                    
                    elif carta.nome in ['Avanço 10']:
                        cartas_slot_c.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 850  
                        nova_posicao_y = 70  
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)
                        nova_posicao = posicao_bola + 96
                        posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao))
                       
                    
                    elif carta.nome in ['Avanço 15']:
                        cartas_slot_c.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 850  
                        nova_posicao_y = 70  
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)
                        nova_posicao = posicao_bola + 144
                        posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao))
                        
                    
                                            
                    elif carta.nome in ['Meio campo']:
                        cartas_slot_c.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 850  
                        nova_posicao_y = 70  
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)
                        posicao_bola = 480
                              
                    
                    elif carta.nome in ['Lesão']:
                        cartas_slot_c.append(carta)
                        cartas_na_mao.remove(carta)                       
                        nova_posicao_x = 850  
                        nova_posicao_y = 70  
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)
                        if cartas_na_mao_inimigo:
                                carta_removida = random.choice(cartas_na_mao_inimigo)
                                cartas_na_mao_inimigo.remove(carta_removida)
                    
                    elif carta.nome in ['Torcida']:
                        cartas_slot_c.append(carta)
                        cartas_na_mao.remove(carta)                       
                        nova_posicao_x = 850  
                        nova_posicao_y = 70  
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)
   
                        
                    elif carta.nome in ['Chute livre', 'Penalti', 'Gol de ouro']:
                        cartas_slot_a.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 280  
                        nova_posicao_y = 217 
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)  
                        
                        
                    
                    elif carta.nome in ['Goleiro', 'Pressão']:
                        cartas_slot_b.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 600  
                        nova_posicao_y = 217 
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y) 
                        
                    
                    turno_jogador = False
                    contador_turnos += 1 
                    

    if not turno_jogador and pygame.time.get_ticks() - tempo_espera_bot>= tempo_espera_bot_fixo:
        carta_bot = escolher_carta_bot(cartas_na_mao_inimigo)  
        if carta_bot:
            if carta_bot.nome in ['Chute livre', 'Penalti', 'Gol de ouro']:
                cartas_slot_b.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 280  
                nova_posicao_y_bot = 217 
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                                
            elif carta_bot.nome in ['Avanço 5']:
                cartas_slot_c.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 850  
                nova_posicao_y_bot = 70  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                nova_posicao1 = posicao_bola - 48
                posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao1))
            
            elif carta_bot.nome in ['Avanço 10']:
                cartas_slot_c.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 850  
                nova_posicao_y_bot = 70  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                nova_posicao1 = posicao_bola - 96 
                posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao1)) 
            
            elif carta_bot.nome in [ 'Avanço 15']:
                cartas_slot_c.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 850  
                nova_posicao_y_bot = 70  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                nova_posicao1 = posicao_bola - 144
                posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao1))  
            
            elif carta_bot.nome in ['Meio campo']:
                cartas_slot_c.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 850  
                nova_posicao_y_bot = 70  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                posicao_bola = 480   
                
            elif carta_bot.nome in ['Lesão']:
                cartas_slot_c.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 850  
                nova_posicao_y_bot = 70  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                if cartas_na_mao:
                    carta_removida = random.choice(cartas_na_mao)
                    cartas_na_mao.remove(carta_removida) 
            
            elif carta_bot.nome in ['Torcida']:
                cartas_slot_c.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 850  
                nova_posicao_y_bot = 70  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                                           
                            
            elif carta_bot.nome in ['Goleiro', 'Pressão']:
                cartas_slot_a.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 600  
                nova_posicao_y_bot = 217  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                                
        contador_turnos += 1 
                            
        if contador_turnos >= 1 and not turno_jogador:
            if len(deck_inimigo.cartas) > 0:
             # Adiciona uma carta do deck à mão do bot
             carta_comprada_bot = deck_inimigo.cartas.pop(0)
             cartas_na_mao_inimigo.append(carta_comprada_bot)
                           
        turno_jogador = True
        tempo_espera_bot = pygame.time.get_ticks()  # Atualiza o tempo de espera do bot
         
         # Calcular a porcentagem de conclusão do trajeto
        percentual_conclusao = arredondar_percentual(((posicao_bola - limite_minimo) / (limite_maximo - limite_minimo)) * 100)
        
        # Realizar a "roleta"
        chance_vitoria_jogador = 100 - percentual_conclusao
        chance_vitoria_bot = percentual_conclusao

        # Realizar a "roleta"
        vencedor = "jogador" if random.randint(1, 100) <= chance_vitoria_jogador else "bot"

        # Exibir o resultado
        print(f"Porcentagem de conclusão: {percentual_conclusao}%")
        print(f"Chances de vitória: Jogador = {chance_vitoria_jogador}%, Bot = {chance_vitoria_bot}%")
        print(f"Vencedor: {vencedor}")
        
        
        
    # Lógica de compra de cartas apenas no turno do jogador
    if contador_turnos >= 1 and turno_jogador:
        if len(cartas_no_deck) > 0  :
            # Adiciona uma carta do deck à mão do jogador
            carta_comprada = cartas_no_deck.pop(0)
            cartas_na_mao.append(carta_comprada)
               
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
    
    screen.blit(Bola, (posicao_bola, 390))
    
    if turno_jogador:
        screen.blit(mensagem_turno, (440, 513))
            
    pygame.display.update()
    clock.tick(60)

