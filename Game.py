import pygame
import sys
import random
import os
from EditorDeck import carregar_deck_usuario , criar_cartas_disponiveis , Deck
from Classes.carta import Carta
from Classes.Bot import escolher_carta_bot

brown_color = (73, 49, 49)
yellow_color = (248, 245, 28)
red_color = (251, 7, 7)
white_color = (255, 255, 255)
black_color = (0, 0, 0)

button_font = pygame.font.Font('Fontes/Bahnschrift.ttf', 24)
rectangle = pygame.Surface((305, 755))
rectangle.fill(brown_color)

pygame.init()
screen_width, screen_height = 1043, 755
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Fut Champions')
clock = pygame.time.Clock()

mensage_font = pygame.font.Font('Fontes/FRAHV.TTF', 24)
mensage_font2 = pygame.font.Font('Fontes/FRAHV.TTF', 70)
mensage_font1 = pygame.font.Font('Fontes/Bahnschrift.ttf', 44)
mensagem_turno = mensage_font.render('É a sua vez!', True, (255, 255, 255))

mensagem_gol = mensage_font1.render('GOOOLLL!', True, (255, 255, 0))
mensagem_errou = mensage_font1.render('ERROOU!', True, (255, 255, 0))
mensagem_p = mensage_font1.render('Preparando chute...', True, (255, 255, 0))

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
tempo_espera_bot_fixo = 5000
contador_turnos = 0
contador_turnos2 = 0

posicao_bola = 480
limite_minimo = 130
limite_maximo = 830

def calcular_porcentagem(posicao_bola, limite_minimo, limite_maximo):
    # Calcula a porcentagem com base na posição da bola e limites
    percentual = ((posicao_bola - limite_minimo) / (limite_maximo - limite_minimo)) * 100
    # Arredonda para o múltiplo de 5 mais próximo
    percentual_arredondado = round(percentual / 5) * 5
    # Garante que o percentual esteja entre 0% e 100%
    percentual_final = max(0, min(100, percentual_arredondado))
    return percentual_final

def calcular_vencedor(percentual_jogador, percentual_bot):
    # Gera um número aleatório entre 0 e 100
    numero_aleatorio = random.randint(0, 100)

    # Verifica em qual intervalo o número aleatório se encontra
    if numero_aleatorio <= percentual_jogador:
        return "Jogador"
    elif numero_aleatorio <= percentual_jogador + percentual_bot:
        return "Bot"

ultima_posicao_carta_jogada = (0, 0)
ultima_posicao_carta_jogada_bot = (0, 0)

def renderizar_texto(texto, posicao, cor=(255, 255, 255), tamanho=70):
    fonte = pygame.font.Font( 'Fontes/FRAHV.TTF', tamanho)
    texto_renderizado = fonte.render(texto, True, cor)
    screen.blit(texto_renderizado, posicao)

percentual_jogador = 50  # Defina um valor padrão inicial
percentual_bot = 50

pontos_jogador = 0
pontos_bot = 0

def piscar_texto(texto, fonte, cor, posicao, frequencia):
    now = pygame.time.get_ticks()
    mostra_texto = (now // frequencia) % 2 == 0
    if mostra_texto:
        texto_surface = fonte.render(texto, True, cor)
        screen.blit(texto_surface, posicao)
 
vencedor = None       

gol = None
errou = None

nome_ultima_carta_jogada_bot = ""
nome_ultima_carta_jogada_jogador = ""

ambos_sem_cartas = False

# Adicione esta função para verificar se ambos os jogadores não têm mais cartas
def ambos_sem_cartas_na_mao(cartas, cartas_bot):
    return not cartas and not cartas_bot

largura, altura = 990, 400

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

btn_width = 232
btn_height = 41
# Calcula a posição central horizontal da tela
center_x = 500
button_voltar, button_rect1 = create_button(
    'Voltar', button_font, black_color, white_color,
    btn_width, btn_height, (center_x, 450)
)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
           if button_rect1.collidepoint(event.pos):
                pygame.quit()
                Menu_script = os.path.join(os.path.dirname(__file__), "Menu_inicial.py")
                os.system(f"python {Menu_script}")
                sys.exit()
           
           if turno_jogador: 
            gol = False
            errou = False
            vencedor = False
             
            for carta in cartas_na_mao:
                if carta.rect.collidepoint(event.pos):
                    # Verifica se o nome da carta está na lista permitida
                    if carta.nome in ['Avanço 5']:
                        cartas_slot_c.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 850  
                        nova_posicao_y = 70  
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)
                        nova_posicao = posicao_bola + 35
                        posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao))
                        percentual_jogador = percentual_jogador + 5
                        
                    
                    elif carta.nome in ['Avanço 10']:
                        cartas_slot_c.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 850  
                        nova_posicao_y = 70  
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)
                        nova_posicao = posicao_bola + 70
                        posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao))
                        percentual_jogador = percentual_jogador + 10
                       
                    
                    elif carta.nome in ['Avanço 15']:
                        cartas_slot_c.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 850  
                        nova_posicao_y = 70  
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)
                        nova_posicao = posicao_bola + 105
                        posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao))
                        percentual_jogador = percentual_jogador + 15
                        
                    
                                            
                    elif carta.nome in ['Meio campo']:
                        cartas_slot_c.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 850  
                        nova_posicao_y = 70  
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)
                        posicao_bola = 480
                        percentual_jogador =  50
                              
                    
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
                        nova_posicao = posicao_bola + 175
                        posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao))
                        percentual_jogador = percentual_jogador + 25
                        percentual_bot = percentual_bot -25
   
                        
                    elif carta.nome in ['Chute livre']:
                        cartas_slot_a.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 280  
                        nova_posicao_y = 217 
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)  
                        ultima_posicao_carta_jogada = carta.rect.topleft
                    
                    elif carta.nome in ['Penalti']:
                        cartas_slot_a.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 280  
                        nova_posicao_y = 217 
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)  
                        ultima_posicao_carta_jogada = carta.rect.topleft   
                    
                    elif carta.nome in ['Gol de ouro']:
                        cartas_slot_a.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 280  
                        nova_posicao_y = 217 
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y)  
                        ultima_posicao_carta_jogada = carta.rect.topleft     
                                           
                    elif carta.nome in ['Goleiro']:
                        cartas_slot_b.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 600  
                        nova_posicao_y = 217 
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y) 
                        ultima_posicao_carta_jogada = carta.rect.topleft
                        
                    elif carta.nome in ['Pressão']:
                        cartas_slot_b.append(carta)
                        cartas_na_mao.remove(carta)
                        nova_posicao_x = 600  
                        nova_posicao_y = 217 
                        carta.rect.topleft = (nova_posicao_x, nova_posicao_y) 
                        ultima_posicao_carta_jogada = carta.rect.topleft    
                    
                    nome_ultima_carta_jogada_jogador = carta.nome
                    turno_jogador = False
                    contador_turnos += 1 
           
           if turno_jogador and not cartas_na_mao:
            
             turno_jogador = False
             contador_turnos += 1
                        
                    
                    
                
    if not turno_jogador and pygame.time.get_ticks() - tempo_espera_bot>= tempo_espera_bot_fixo:
        carta_bot = escolher_carta_bot(cartas_na_mao_inimigo)  
        if carta_bot:
            if carta_bot.nome in ['Chute livre']:
                cartas_slot_b.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 600  
                nova_posicao_y_bot = 217 
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                ultima_posicao_carta_jogada_bot = carta_bot.rect.topleft
            
            elif carta_bot.nome in ['Penalti']:
                cartas_slot_b.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 600  
                nova_posicao_y_bot = 217 
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                ultima_posicao_carta_jogada_bot = carta_bot.rect.topleft    
            
            elif carta_bot.nome in ['Gol de ouro']:
                cartas_slot_b.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 600 
                nova_posicao_y_bot = 217 
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                ultima_posicao_carta_jogada_bot = carta_bot.rect.topleft    
                                
            elif carta_bot.nome in ['Avanço 5']:
                cartas_slot_c.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 850  
                nova_posicao_y_bot = 70  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                nova_posicao1 = posicao_bola - 35
                posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao1))
                percentual_bot = percentual_bot + 5
            
            elif carta_bot.nome in ['Avanço 10']:
                cartas_slot_c.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 850  
                nova_posicao_y_bot = 70  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                nova_posicao1 = posicao_bola - 70 
                posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao1)) 
                percentual_bot = percentual_bot + 10
            
            elif carta_bot.nome in [ 'Avanço 15']:
                cartas_slot_c.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 850  
                nova_posicao_y_bot = 70  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                nova_posicao1 = posicao_bola - 105
                posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao1))  
                percentual_bot = percentual_bot + 15
                
            elif carta_bot.nome in ['Meio campo']:
                cartas_slot_c.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 850  
                nova_posicao_y_bot = 70  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                posicao_bola = 480   
                percentual_bot = 50
                
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
                nova_posicao1 = posicao_bola - 175
                posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao1))
                percentual_bot = percentual_bot + 25
                percentual_jogador = percentual_jogador -25
                                           
                            
            elif carta_bot.nome in ['Goleiro']:
                cartas_slot_a.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 280  
                nova_posicao_y_bot = 217  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                ultima_posicao_carta_jogada_bot = carta_bot.rect.topleft
            
            elif carta_bot.nome in ['Pressão']:
                cartas_slot_a.append(carta_bot)
                cartas_na_mao_inimigo.remove(carta_bot)
                nova_posicao_x_bot = 280  
                nova_posicao_y_bot = 217  
                carta_bot.rect.topleft = (nova_posicao_x_bot, nova_posicao_y_bot)
                ultima_posicao_carta_jogada_bot = carta_bot.rect.topleft    
            
            nome_ultima_carta_jogada_bot = carta_bot.nome    
            
        ambos_sem_cartas = ambos_sem_cartas_na_mao(cartas_na_mao, cartas_na_mao_inimigo)      
        contador_turnos += 1 
                            
        if contador_turnos >= 1 and not turno_jogador:
            if len(deck_inimigo.cartas) > 0:
             # Adiciona uma carta do deck à mão do bot
             carta_comprada_bot = deck_inimigo.cartas.pop(0)
             cartas_na_mao_inimigo.append(carta_comprada_bot)
        
        
                 
        turno_jogador = True
        tempo_espera_bot = pygame.time.get_ticks()  # Atualiza o tempo de espera do bot
         
        percentual_jogador = calcular_porcentagem(posicao_bola, limite_minimo, limite_maximo)
        percentual_bot = 100 - percentual_jogador
        
        vencedor = calcular_vencedor(percentual_jogador, percentual_bot)
        
        print(f'Percentual do jogador: {percentual_jogador}%')
        print(f'Percentual do bot: {percentual_bot}%')
        print(f"O vencedor é: {vencedor}")
        
        
    
        
        if vencedor == 'Jogador':
           print("O Jogador ganhou! Verificando Slot A...")
           piscar_texto(f'Jogador: {percentual_jogador}%', mensage_font, (255, 0, 0), (70, 250), 500)
           if ultima_posicao_carta_jogada is not None or ultima_posicao_carta_jogada_bot is not None:
        # Verifica se a última carta jogada está na posição específica com uma tolerância de 5 pixels
           
            if 275 <= ultima_posicao_carta_jogada[0] <= 285 and 212 <= ultima_posicao_carta_jogada[1] <= 222 or 275 <= ultima_posicao_carta_jogada_bot[0] <= 285 and 212 <= ultima_posicao_carta_jogada_bot[1] <= 222:
                print("Há uma carta na posição (280, 217) do slot A!")
                if cartas_slot_a:
                
                 carta_no_slot = cartas_slot_a[-1]  # Pega a última carta adicionada ao slot A
                 print(f"A carta no Slot A é: {carta_no_slot.nome}")
                
                
                 if carta_no_slot.nome == 'Pressão':
                  nova_posicao1 = posicao_bola -175
                  posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao1))
                  percentual_jogador = percentual_jogador -25
                  percentual_bot = percentual_bot + 25
                  cartas_slot_a.remove(carta_no_slot)
                
                 elif carta_no_slot.nome == 'Goleiro':
                  nova_posicao1 = posicao_bola
                  posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao1))
                  percentual_jogador =  35
                  cartas_slot_a.remove(carta_no_slot)
                 
                 elif carta_no_slot.nome == 'Gol de ouro':
                  nova_posicao1 = posicao_bola
                  posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao1))
                  percentual_jogador =  100
                  percentual_bot = 0
                  cartas_slot_a.remove(carta_no_slot)                                  
                  if cartas_na_mao:
                    carta_removida = random.choice(cartas_na_mao)
                    cartas_na_mao.remove(carta_removida)
                 
                 elif carta_no_slot.nome == 'Chute livre':
                   nova_posicao1 = posicao_bola
                   posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao1))
                   percentual_jogador = 75
                   percentual_bot = 25
                   cartas_slot_a.remove(carta_no_slot)
                 
                 elif carta_no_slot.nome == 'Penalti':
                   nova_posicao1 = posicao_bola
                   posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao1))
                   percentual_jogador = 85
                   percentual_bot = 15
                   cartas_slot_a.remove(carta_no_slot)      
                  
                    
                  
                  
                 
                 
                if percentual_jogador >= random.randint(0, 100):
                    print("GOL! O Jogador marcou!")
                    pontos_jogador += 1
                    posicao_bola = 480
                    percentual_bot = 50
                    percentual_jogador = 50
                    gol = True

                else:
                    print("Errou! O Jogador não marcou.")
                    errou = True

            elif percentual_jogador >= random.randint(0, 100):
                print("GOL! O Jogador marcou!")
                pontos_jogador += 1
                posicao_bola = 480
                percentual_bot = 50
                percentual_jogador = 50
                gol = True

            else:
                print("Errou! O Jogador não marcou.")
                errou = True
                 
                   
        if vencedor == 'Bot':
           print("O Bot ganhou! Verificando Slot B...")
           piscar_texto(f'Bot: {percentual_bot}%', mensage_font, (255, 0, 0), (760, 250), 500)
           if ultima_posicao_carta_jogada_bot is not None or ultima_posicao_carta_jogada is not None:
             # Verifica se a última carta jogada está na posição específica com uma tolerância de 5 pixels
              if 595 <= ultima_posicao_carta_jogada_bot[0] <= 605 and 212 <= ultima_posicao_carta_jogada_bot[1] <= 222 or 595 <= ultima_posicao_carta_jogada[0] <= 605 and 212 <= ultima_posicao_carta_jogada[1] <= 222:
                print("Há uma carta na posição (600, 217) do slot B!")
                if cartas_slot_b:
                 carta_no_slot1 = cartas_slot_b[-1]  # Pega a última carta adicionada ao slot B
                 print(f"A carta no Slot B é: {carta_no_slot1.nome}")
                 if carta_no_slot1.nome == 'Pressão':
                  nova_posicao2 = posicao_bola + 175
                  posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao2))
                  percentual_bot = percentual_bot - 25
                  percentual_jogador = percentual_jogador + 25
                  cartas_slot_b.remove(carta_no_slot1)
                
                 elif carta_no_slot1.nome == 'Goleiro':
                  nova_posicao2 = posicao_bola
                  posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao2))
                  percentual_bot = 35
                  cartas_slot_b.remove(carta_no_slot1)   
                 
                 elif carta_no_slot1.nome == 'Gol de ouro':
                  nova_posicao2 = posicao_bola
                  posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao2))
                  percentual_jogador = 0
                  percentual_bot = 100
                  cartas_slot_b.remove(carta_no_slot1)                                  
                  if cartas_na_mao_inimigo:
                    carta_removida = random.choice(cartas_na_mao_inimigo)
                    cartas_na_mao_inimigo.remove(carta_removida)
                 
                 elif carta_no_slot1.nome == 'Chute livre':
                   nova_posicao2 = posicao_bola
                   posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao2))
                   percentual_jogador = 25
                   percentual_bot = 75
                   cartas_slot_b.remove(carta_no_slot1) 
                 
                 elif carta_no_slot1.nome == 'Penalti':
                   nova_posicao2 = posicao_bola
                   posicao_bola = max(limite_minimo, min(limite_maximo, nova_posicao2))
                   percentual_jogador = 15
                   percentual_bot = 85
                   cartas_slot_b.remove(carta_no_slot1)   
                   
                     
                  
                
                if percentual_bot >= random.randint(0, 100):
                   
                                     
                   print("GOL! o bot marcou!")                    
                   pontos_bot += 1
                   posicao_bola = 480
                   percentual_bot = 50
                   percentual_jogador = 50
                   
                   gol = True
                   
                else:                   
                   
                   print("Errou! o  bot não marcou!")
                   errou = True
                     
                   
              elif percentual_bot >= random.randint(0, 100):
                  
                  print("GOL! o  bot marcou!")                   
                                    
                  tempo_inicio_mensagem = pygame.time.get_ticks()
                  tempo_decorrido_mensagem = 0
                  pontos_bot += 1
                 
                  posicao_bola = 480
                  percentual_bot = 50
                  percentual_jogador = 50
                  gol = True
              
              else:    
                print("Errou! o  bot não marcou!")
                errou = True
             
                  
                 
      
        
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
    
    renderizar_texto(f' {percentual_jogador}%', (70, 250))
    renderizar_texto(f' {percentual_bot}%', (760, 250))

    renderizar_texto(f' {pontos_jogador} x {pontos_bot} ', (400, 230))
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    button_rect1_color = black_color if not button_rect1.collidepoint(mouse_x, mouse_y) else red_color
    
    if vencedor:
        if vencedor == 'Jogador':
            now = pygame.time.get_ticks()
            mostra_texto = (now // 500) % 2 == 0
            
            if mostra_texto:
                texto_surface = mensage_font2.render(f' {percentual_jogador}%', True, (255, 255, 0))
                screen.blit(texto_surface, (70, 250))
        elif vencedor == 'Bot':
            now = pygame.time.get_ticks()
            mostra_texto_bot = (now // 500) % 2 == 0
           
            if mostra_texto_bot:
                texto_surface_bot = mensage_font2.render(f' {percentual_bot}%', True, (255, 255, 0))
                screen.blit(texto_surface_bot, (760, 250))
    
    
    if turno_jogador:
        screen.blit(mensagem_turno, (440, 513))
    else:
        screen.blit(mensagem_p, (320, 170))
          
    if gol:
        
        screen.blit(mensagem_gol, (400, 170))  
    elif errou:
        
        screen.blit(mensagem_errou, (400, 170))          
    renderizar_texto(f'Carta jogada_Bot: {nome_ultima_carta_jogada_bot}', (400, 0), cor=(255, 255, 255), tamanho=15) 
    renderizar_texto(f'Carta jogada: {nome_ultima_carta_jogada_jogador}', (400, 730), cor=(255, 255, 255), tamanho=15)  
    
    if ambos_sem_cartas:
        pygame.draw.rect(screen, (73, 49, 49), (250, 150, 500, 400))  # Cores: (vermelho, verde, azul)
        screen.blit(button_voltar, button_rect1)
        pygame.draw.rect(screen, button_rect1_color, button_rect1, 2)
    
    if ambos_sem_cartas:
        if pontos_jogador > pontos_bot:
            mensagem = "Você ganhou!"
        elif pontos_jogador < pontos_bot:
            mensagem = "Você perdeu!"
        else:
            mensagem = "Empate!"
        
        mensagem += f" {pontos_jogador} x {pontos_bot}"
    else:
        mensagem = ""
    
    if mensagem:
        fonte = mensage_font1
        texto = fonte.render(mensagem, True, (255, 255, 255))
        screen.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2 - texto.get_height() // 2))
    
  
    pygame.display.update()
    clock.tick(60)

