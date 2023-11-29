import pygame
import sys
import os
from Classes.carta import Carta
from Classes.deck import Deck
from Classes.carta_ampliada import CartaAumentada
from Classes.Descriçao import DescricaoCarta


nome_fonte = "BAHNSCHRIFT.TTF"
caminho_fonte = os.path.join(os.path.dirname(__file__), "Fontes", nome_fonte)

# Inicialização do Pygame
pygame.init()

# Definir constantes
WIDTH, HEIGHT = 1043, 755
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
pygame.display.set_caption("Fut Champions")


font = pygame.font.Font(caminho_fonte, 36)


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

class Button:
    def __init__(self):
        self.left = 40
        self.top = 460
        self.length = 232
        self.height = 41
        self.normal_color = [73, 49, 49]
        self.hover_color = [10, 16, 28]
        self.color = self.normal_color
        self.text_color = [255, 255, 255]
        self.mouse_was_pressed = False
        self.text_size = 30
        self.text = "Salvar/Sair"

    def render(self):
        retangulo = pygame.Rect(self.left, self.top, self.length, self.height)
        mouse_got_pressed = pygame.mouse.get_pressed()[0]
        self.mouse_was_clicked = mouse_got_pressed and not self.mouse_was_pressed

        self.mouse_was_pressed = mouse_got_pressed
        mouse_left, mouse_top = pygame.mouse.get_pos()

        is_mouse_collision = retangulo.collidepoint(mouse_left, mouse_top)
        self.color = self.hover_color if is_mouse_collision else self.normal_color

        font = pygame.font.Font(None, self.text_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.left + self.length / 2, self.top + self.height / 2))

        pygame.draw.rect(screen, self.color, retangulo)
        screen.blit(text_surface, text_rect)

    def get_clicked(self):
        return self.mouse_was_clicked

button = Button()

# Função principal
def main():
    # Crie um deck para o jogador com limite máximo de 8 cartas
    deck_jogador = Deck()

    # Crie algumas cartas disponíveis
    cartas_disponiveis = criar_cartas_disponiveis()
    
    
    
    # Crie uma lista para armazenar os slots vazios
    slots_vazios = [
        (50, 580, 100, 150),  
        (170, 580, 100, 150),
        (290, 580, 100, 150),
        (410, 580, 100, 150),
        (530, 580, 100, 150),
        (650, 580, 100, 150),
        (770, 580, 100, 150),
        (890, 580, 100, 150),
        
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
        slot_start_x = 50
        slot_start_y = 580
        
        # Atualizar a tela
        all_sprites.update()
        
        
        # Desenhar na tela
        screen.fill(DARK_BLUE)
        
        desenhar_slots(screen, slots_vazios)  # Desenha os slots antes das cartas
        
        pygame.draw.rect(screen, DARK_RED, (0, 550, 1100, 250))  # (x, y, largura, altura)
        
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
         
        button.render()
        
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
