from player import Player
from aiplayer import AiPlayer
from settings import Setting


class FingerGame:
    """Class for game action and resources"""

    def __init__(self, if_ai1=0, if_ai2=0):
        self.setting = Setting()
        if if_ai1:
            self.player1 = AiPlayer(self, 1)
        else:
            self.player1 = Player(self, 1)
        if if_ai2:
            self.player2 = AiPlayer(self, 2)
        else:
            self.player2 = Player(self, 2)
        self.if_ai = [if_ai1, if_ai1]
        self.current_player = self.player1
        self.waiting_player = self.player2

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
            return self.player1 if self.player2.HP <= 0 else self.player2

    def change_term(self):
        player = self.current_player
        self.current_player = self.waiting_player
        self.waiting_player = player

    def make_move(self, move=None):
        result = self.current_player.take_step(self.waiting_player, move)
        if result != "pause":
            self.change_term()

    def run_game(self):
        """Start game"""
        while True:
            # Player1's round
            self.current_player = self.player1      # For indication
            self.waiting_player = self.player2
            while True:
                result = self.player1.take_step(self.player2)
                if result == "pause" or result == "error":
                    continue
                else:
                    break
            if self.is_dead():
                break

            # Player2's round
            self.current_player = self.player2      # For indication
            self.waiting_player = self.player1
            while True:
                result = self.player2.take_step(self.player1)
                if result == "pause" or result == "error":
                    continue
                else:
                    break
            if self.is_dead():
                break


if __name__ == '__main__':
    game = FingerGame(if_ai1=0, if_ai2=0)
    game.run_game()
