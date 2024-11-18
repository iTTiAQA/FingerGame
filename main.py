from MCTS import MCTS
from fingergame import FingerGame
from source import super_input


class FingerGame2(FingerGame):
    def __init__(self, if_ai1=0, if_ai2=0):
        super().__init__(if_ai1, if_ai2)

    def run_game(self):
        while True:
            # Player1's round
            self.current_player = self.player1      # For indication
            self.waiting_player = self.player2

            while True:
                self.display()
                if self.if_ai[0]:
                    ai1 = MCTS(self, 1, self.setting.iterations)
                    print("1's round")
                    move = ai1.run().move
                    result = self.player1.take_step(self.player2, move)
                    print(f"1's move: {move}")
                else:
                    result = self.player1.take_step(self.player2)

                print(f"step state:{result}")
                if result == "pause" or result == "error":
                    continue
                else:
                    break

            if self.is_dead():
                self.display()
                print("2 lose")
                break

            # Player2's round
            self.current_player = self.player2      # For indication
            self.waiting_player = self.player1

            while True:
                self.display()
                if self.if_ai[1]:
                    ai2 = MCTS(self, 2, self.setting.iterations)
                    print("2's round")
                    move = ai2.run().move
                    result = self.player2.take_step(self.player1, move)
                    print(f"2's move: {move}")
                else:
                    result = self.player2.take_step(self.player1)

                print(f"step state:{result}")
                if result == "pause" or result == "error":
                    continue
                else:
                    break

            if self.is_dead():
                self.display()
                print("1 lose")
                break


if __name__ == "__main__":
    _if_ai1 = super_input(["yes", "no"], "if player1 is ai(yes/no):")
    _if_ai2 = super_input(["yes", "no"], "if player2 is ai(yes/no):")
    _if_ai1 = 0 if _if_ai1 == "no" else 1
    _if_ai2 = 0 if _if_ai2 == "no" else 1

    game = FingerGame2(if_ai1=_if_ai1, if_ai2=_if_ai2)
    game.run_game()
