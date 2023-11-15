import player


class Dealer(player.Player):
    def play(self) -> str:
        '''The dealer plays his turn and he has to hit when his score is 16 or below'''
        string = ""
        while True: 
            string += "\nDealer's Hand:\n"
            string += str(self) + "\n"    
            if self.score() <= 16:
                self.hit()
                string += "Dealer Hits!\n"    # added rn
            else:
                break
        if self.score() > 21:
            string += "Bust!!!!!\n"
        return string
