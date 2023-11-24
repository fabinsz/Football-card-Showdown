import pygame
import sys
from Classes.carta import Carta
from Classes.deck import Deck

# Inicialização do Pygame
pygame.init()

# Definir constantes
WIDTH, HEIGHT = 1000, 800
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19) 
YELLOW = (255, 255, 0)

# Configurar a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football card Showdown")

# Fonte para o texto
font = pygame.font.Font(None, 36)


def criar_cartas_disponiveis():
    cartas_disponiveis = [
        Carta("Carta 1", 50, 50),
        Carta("Carta 2", 170, 50),
        Carta("Carta 3", 290, 50),
        Carta("Carta 2", 170, 50),  
        Carta("Carta 3", 290, 50),  
        Carta("Carta 1", 50, 50),  
        Carta("Carta 2", 170, 50),  
        Carta("Carta 3", 290, 50),  
        Carta("Carta 1", 50, 50),
        Carta("Carta 4", 410, 50),
        Carta("Carta 4", 410, 50),
    ]
    return cartas_disponiveis

def desenhar_slots(screen, slots_vazios):
    for slot in slots_vazios:
        pygame.draw.rect(screen, WHITE, slot)

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
    
    carta_em_arrasto = None  # Variável para rastrear qual carta está sendo arrastada
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
                            # Remove a carta do deck
                            deck_jogador.remover_carta(carta_em_arrasto)
                           


            # Adicione esta parte para lidar com o efeito de brilho
            elif event.type == pygame.MOUSEMOTION:
                for carta in all_sprites:
                    if carta.rect.collidepoint(pygame.mouse.get_pos()):
                        carta.brilhar()
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
        screen.fill(WHITE)
        
        desenhar_slots(screen, slots_vazios)  # Desenha os slots antes das cartas
        
        pygame.draw.rect(screen, BROWN, (0, 550, 1000, 250))  # (x, y, largura, altura)
        
        # Desenhar os retângulos brancos usando um loop
        for i in range(8):
         x = slot_start_x + i * slot_spacing
         pygame.draw.rect(screen, WHITE, (x, slot_start_y, slot_width, slot_height))
        
        # Atualizar posição da carta sendo arrastada
        if carta_em_arrasto:
            carta_em_arrasto.update()        
                
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
