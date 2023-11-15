import card
import random


class Deck:
    def __init__(self) -> None:
        '''Initalizing class deck that has 52 cards'''
        self.deck = []
        for rank in range(13):
            for suit in range(4):
                self.deck.append(card.Card(rank, suit))

    
    def shuffle(self):
        '''Shuffle or randomizes the position of every card'''
        random.shuffle(self.deck)


    def draw_card(self):
        '''Take a card out of the deck and returns it'''
        return self.deck.pop(len(self.deck) - 1)


    def __len__(self):
        '''Returns the number of cards in the deck'''
        return len(self.deck)