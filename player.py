import deck


class Player:
    def __init__(self, deck):
        self._deck = deck
        self._hand = []
        self.hit()
        self.hit()
        self._hand.sort()
    
    
    def hit(self):
        '''Pull a card from the deck and put in the hand of the player'''
        # card = self._deck.draw_card()
        # self._hand.append(card)
        self._hand.sort()
        card_drawn = self._deck.draw_card()
        self._hand.append(card_drawn)
        return card_drawn
    
    def score(self):
        '''Calculate the score of the player's hand'''
        score = 0
        has_ace = False
        for card in self._hand:
            rank = card.rank
            if rank < 9:
                score += rank + 2
            elif rank != 12:
                score += 10
            else:
                has_ace = True
                score += 1

        new_score = score + 10
        # new_score = score + (counter * 10)
        if has_ace is True and new_score <= 21:
            return new_score
        else:
            return score
    
    
    def __str__(self) -> str:
        '''Print statement for player object'''
        cards = "\n".join(str(card) for card in self._hand)
        score = f"\nScore = {self.score()}"
        return cards + score