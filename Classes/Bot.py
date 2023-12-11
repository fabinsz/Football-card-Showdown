import random


# Função para o bot escolher uma carta
def escolher_carta_bot(cartas_na_mao_inimigo):
    # Implemente a lógica desejada para a escolha do bot
    if cartas_na_mao_inimigo:
        return random.choice(cartas_na_mao_inimigo)
    else:
        return None  # Retorna None se o bot não tiver cartas na mão

      