import pygame
import sys
from Classes.carta import Carta
from Classes.deck import Deck

# Inicialização do Pygame
pygame.init()

# Definir constantes
WIDTH, HEIGHT = 800, 600
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurar a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football card Showdown")

# Fonte para o texto
font = pygame.font.Font(None, 36)


def criar_cartas_disponiveis():
    cartas_disponiveis = [
        Carta("Carta 1", 50, 50),
        Carta("Carta 2", 250, 50),
        Carta("Carta 3", 450, 50),
        Carta("Carta 2", 250, 50),  # Carta com o mesmo nome
        Carta("Carta 3", 450, 50),  # Carta com o mesmo nome
        Carta("Carta 1", 50, 50),  # Carta com o mesmo nome
        Carta("Carta 2", 250, 50),  # Carta com o mesmo nome
        Carta("Carta 3", 450, 50),  # Carta com o mesmo nome
        Carta("Carta 1", 50, 50),
        Carta("Carta 4", 650, 50),
        Carta("Carta 4", 650, 50),# Carta com o mesmo nome
    ]
    return cartas_disponiveis

# Função principal
def main():
    # Crie um deck para o jogador com limite máximo de 8 cartas
    deck_jogador = Deck()

    # Crie algumas cartas disponíveis
    cartas_disponiveis = criar_cartas_disponiveis()

    # Crie um grupo de sprites para as cartas
    all_sprites = pygame.sprite.Group()
    all_sprites.add(*cartas_disponiveis)

    # Lista de mensagens
    mensagens = []

    # Cooldown para evitar cliques rápidos
    cooldown = 500  # em milissegundos
    last_click_time = 0

    # Interface para o jogador escolher as cartas
    running = True
    clock = pygame.time.Clock()
    while running:
        # Lidar com eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                current_time = pygame.time.get_ticks()
                if current_time - last_click_time > cooldown:
                   # Verificar se o deck está cheio
                  if not deck_jogador.deck_cheio:
                    # Verificar colisão com os sprites
                    for carta in all_sprites:
                        if carta.rect.collidepoint(pygame.mouse.get_pos()):
                            carta.kill()
                            deck_jogador.adicionar_carta(carta)
                            mensagem = f"{carta.nome} adicionada ao seu deck."
                            mensagens.insert(0, {"texto": mensagem, "tempo": pygame.time.get_ticks()})  # Adiciona a mensagem no início da lista
                            last_click_time = current_time  # Atualizar o tempo do último clique
                            break  # Saia do loop após adicionar uma carta ao deck

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

        # Limitar o número de mensagens a serem exibidas
        mensagens = mensagens[:1]

        # Atualizar a tela
        all_sprites.update()

        # Desenhar na tela
        screen.fill(WHITE)
        all_sprites.draw(screen)

        # Exibir a mensagem de deck cheio na tela, se aplicável
        if deck_jogador.deck_cheio:
            mensagem_deck_cheio = font.render("Deck cheio! Não é possível adicionar mais cartas.", True, BLACK)
            screen.blit(mensagem_deck_cheio, (100, 550))

        # Exibir as mensagens mais recentes na tela
        y_pos = 10 if deck_jogador.deck_cheio else 10
        mensagens_a_remover = []
        for i, mensagem_info in enumerate(mensagens):
            tempo_atual = pygame.time.get_ticks()
            tempo_inicial = mensagem_info["tempo"]
            duracao = 1000

            if tempo_atual < tempo_inicial + duracao:
                texto = font.render(mensagem_info["texto"], True, BLACK)
                screen.blit(texto, (10, y_pos))
                y_pos += 30
            else:
                mensagens_a_remover.append(i)

        # Remove as mensagens expiradas da lista
        for i in mensagens_a_remover:
            mensagens.pop(i)

        # Atualizar a tela
        pygame.display.flip()

        # Define o FPS
        clock.tick(FPS)

    # Encerrar o Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
