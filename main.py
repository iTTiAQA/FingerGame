from player import Player


class FingerGame:
    """Class for game action and resources"""

    def __init__(self):
        self.player1 = Player(self, 1)
        self.player2 = Player(self, 2)

    def display(self):
        print("\n")
        print("Player1:")
        print(f"Shield:{self.player1.shield}    HP:{self.player1.HP}    "
              f"Left:{self.player1.left}    Right:{self.player1.right}")
        print("Player2:")
        print(f"Shield:{self.player2.shield}    HP:{self.player2.HP}    "
              f"Left:{self.player2.left}    Right:{self.player2.right}")

    def is_dead(self):
        if self.player1.HP <= 0 or self.player2.HP <= 0:
            return True

    def run_game(self):
        """Start game"""
        while True:
            # Player1's round
            while True:
                result = self.player1.take_step(self.player2)
                if result == "pause" or result == "error":
                    continue
                else:
                    break
            if self.is_dead():
                break

            # Player2's round
            while True:
                result = self.player2.take_step(self.player1)
                if result == "pause" or result == "error":
                    continue
                else:
                    break
            if self.is_dead():
                break


if __name__ == '__main__':
    game = FingerGame()
    game.run_game()
