import pygame
import sys
from Classes.carta import Carta
from Classes.deck import Deck
from Classes.carta_ampliada import CartaAumentada
from Classes.Descriçao import DescricaoCarta


# Inicialização do Pygame
pygame.init()

# Definir constantes
WIDTH, HEIGHT = 1000, 800
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_RED = (73, 49, 49) 
YELLOW = (255, 255, 0)
LIGHT_GRAY = (217, 217, 217)
DARK_GRAY = (169, 169, 169)
DARK_BLUE = (10, 16, 28)


# Configurar a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football card Showdown")

# Fonte para o texto
font = pygame.font.Font(None, 36)


def criar_cartas_disponiveis():
    cartas_disponiveis = [
        Carta("Carta 1", 410, 50, BLACK, "teste teste"),  # Cor preta
        Carta("Carta 2", 530, 50, (0, 0, 255), "teste teste!"),  # Cor azul
        Carta("Carta 3", 650, 50, (255, 0, 0), "teste teste!!"),  # Cor vermelha
        Carta("Carta 2", 530, 50, (0, 0, 255), "teste teste!"),  # Cor azul
        Carta("Carta 3", 650, 50, (255, 0, 0), "teste teste!!"),  # Cor vermelha
        Carta("Carta 1", 410, 50, BLACK, "teste teste"),  # Cor preta
        Carta("Carta 2", 530, 50, (0, 0, 255), "teste teste!"),  # Cor azul
        Carta("Carta 3", 650, 50, (255, 0, 0), "teste teste!!"),  # Cor vermelha
        Carta("Carta 1", 410, 50, BLACK, "teste teste"),  # Cor preta
        Carta("Carta 4", 770, 50, DARK_GRAY, "teste teste!!!"),  
        Carta("Carta 4", 770, 50, DARK_GRAY, "teste teste!!!"),  
    ]
    return cartas_disponiveis

def desenhar_slots(screen, slots_vazios):
    for slot in slots_vazios:
        pygame.draw.rect(screen, LIGHT_GRAY, slot)



# Função principal
def main():
    # Crie um deck para o jogador com limite máximo de 8 cartas
    deck_jogador = Deck()

    # Crie algumas cartas disponíveis
    cartas_disponiveis = criar_cartas_disponiveis()
    
    
    # Crie uma lista para armazenar os slots vazios
    slots_vazios = [
        (30, 600, 100, 150),  
        (150, 600, 100, 150),
        (270, 600, 100, 150),
        (390, 600, 100, 150),
        (510, 600, 100, 150),
        (630, 600, 100, 150),
        (750, 600, 100, 150),
        (870, 600, 100, 150),
        
    ]
    
    
    # Crie um grupo de sprites para as cartas
    all_sprites = pygame.sprite.Group()
    all_sprites.add(*cartas_disponiveis)
        
    
    # Interface para o jogador escolher as cartas
    running = True
    clock = pygame.time.Clock()
    
    # Crie um grupo de sprites para a descrição da carta
    descricao_carta = pygame.sprite.Group()
    
    carta_em_arrasto = None  # Variável para rastrear qual carta está sendo arrastada

    carta_aumentada = None
       

    while running:
        # Lidar com eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse pressionado
                    for carta in all_sprites:
                        if carta.rect.collidepoint(pygame.mouse.get_pos()):
                            carta_em_arrasto = carta
                            carta_em_arrasto.sendo_arrastada = True
                            
                             # Crie uma carta aumentada
                            carta_aumentada = CartaAumentada(carta_em_arrasto)
                            all_sprites.add(carta_aumentada)
                            
                            descricao_carta.add(DescricaoCarta(carta_em_arrasto.descricao, 50, 350))
                            break
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and carta_em_arrasto:
                    carta_em_arrasto.sendo_arrastada = False
                    # Verificar se a carta foi solta dentro de um slot
                    for i, slot in enumerate(slots_vazios):
                        if pygame.mouse.get_pos()[0] in range(slot[0], slot[0] + slot[2]) and \
                           pygame.mouse.get_pos()[1] in range(slot[1], slot[1] + slot[3]):
                            # A carta foi solta dentro de um slot, ajuste a posição e atributos
                            carta_em_arrasto.em_slot = True
                            carta_em_arrasto.slot_rect = slot
                            carta_em_arrasto.rect.topleft = (slot[0], slot[1])  # Ajusta a posição da carta para o canto superior esquerdo do slot
                            deck_jogador.adicionar_carta(carta_em_arrasto)
                            # Remova o slot da lista de slots_vazios
                            slots_vazios.pop(i)
                            descricao_carta.empty()
                            break
                    else:
                        # A carta foi solta fora de um slot, volte para a posição inicial
                        if carta_em_arrasto:  # Verifica se a carta_em_arrasto não é None
                            carta_em_arrasto.rect.topleft = carta_em_arrasto.pos_inicial
                            # Adiciona a carta de volta ao grupo de sprites
                            all_sprites.add(carta_em_arrasto)
                            
                            # Adiciona o slot de volta à lista de slots_vazios
                            x, y, largura, altura = carta_em_arrasto.slot_rect
                            slots_vazios.append((x, y, largura, altura))
                            descricao_carta.empty()
                            # Remove a carta do deck
                            deck_jogador.remover_carta(carta_em_arrasto)
                     # Remova a carta aumentada
                    if carta_aumentada:
                       all_sprites.remove(carta_aumentada)
                       carta_aumentada = None        
                    
                  
                    # Desenhar os retângulos brancos usando um loop
                    for i, carta in enumerate(cartas_disponiveis):
                      x = slot_start_x + i * slot_spacing
                      pygame.draw.rect(screen, carta.cor, (x, slot_start_y, slot_width, slot_height))

            # Adicione esta parte para lidar com o efeito de brilho
            elif event.type == pygame.MOUSEMOTION:
                for carta in all_sprites:
                    if carta.rect.collidepoint(pygame.mouse.get_pos()):
                        carta.brilho = True
                    else:
                        carta.brilho = False
                        

            # Verifique se a tecla "D" foi pressionada
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                deck_jogador.mostrar_cartas()

        # Definir as propriedades dos retângulos brancos
        slot_width, slot_height = 100, 150
        slot_spacing = 120
        slot_start_x = 30
        slot_start_y = 600
        
        # Atualizar a tela
        all_sprites.update()
        
        
        # Desenhar na tela
        screen.fill(DARK_BLUE)
        
        desenhar_slots(screen, slots_vazios)  # Desenha os slots antes das cartas
        
        pygame.draw.rect(screen, DARK_RED, (0, 550, 1000, 250))  # (x, y, largura, altura)
        
        pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, 300, 550))  # (x, y, largura, altura)
        
        # Desenhar os retângulos brancos usando um loop
        for i in range(8):
         x = slot_start_x + i * slot_spacing
         pygame.draw.rect(screen, LIGHT_GRAY, (x, slot_start_y, slot_width, slot_height))
        
        # Atualizar posição da carta sendo arrastada
        if carta_em_arrasto:
            carta_em_arrasto.update()        
                
         # Dentro do loop while running, após o update e antes de desenhar na tela
        descricao_carta.update()
        descricao_carta.draw(screen)
                 
 
        # Desenhar os slots após as cartas
        desenhar_slots(screen, slots_vazios) 
         
        
        all_sprites.draw(screen)      
        
        # Atualizar a tela
        pygame.display.flip()
        

        # Define o FPS
        clock.tick(FPS)

    # Encerrar o Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
