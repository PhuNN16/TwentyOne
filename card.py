class Card:
    def __init__(self, rank, suit) -> None:
        '''Initializing a playing card with attribute rank and suit'''
        self._rank = rank
        self._suit = suit

    @property
    def rank(self):
        '''Accesses the card's rank'''
        return self._rank 

    
    def __str__(self) -> str:
        '''The print statement for the card object'''
        rank = [2, 3, 4, 5, 6, 7, 8 ,9, 10, "Jack", "Queen", "King", "Ace"]
        suit = ["Spades", "Clubs", "Diamonds", "Hearts"]
        return f"{rank[self.rank]} of {suit[self._suit]}"


    def __lt__(self, other):
        ''' Comparing the ranks between two cards'''
        return self.rank < other.rank