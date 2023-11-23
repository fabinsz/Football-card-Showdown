import pygame

class Deck:
    def __init__(self, limite_maximo=8):
        self.limite_maximo = limite_maximo
        self.cartas = []
        self.deck_cheio = False

    def adicionar_carta(self, carta):
        if len(self.cartas) < self.limite_maximo:
            self.cartas.append(carta)
        else:
            self.deck_cheio = True
            print("Seu deck está cheio! Não é possível adicionar mais cartas.")