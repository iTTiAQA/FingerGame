from player import Player
from source import detect_shield
from source import finger_add


class FingerGame:
    """Class for game action and resources"""

    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()

    def display(self):
        print("\n")
        print("Player1:")
        print(f"Shield:{self.player1.shield}    HP:{self.player1.HP}    "
              f"Left:{self.player1.left}    Right:{self.player1.right}")
        print("Player2:")
        print(f"Shield:{self.player2.shield}    HP:{self.player2.HP}    "
              f"Left:{self.player2.left}    Right:{self.player2.right}")

    def super_input(self, choice, string):
        """To simplify the input code"""
        while True:
            self.display()
            _input = input(string)
            if _input in choice:
                return _input

    def is_dead(self):
        if self.player1.HP <= 0 or self.player2.HP <= 0:
            return True

    def a_step_player1(self):
        or_left = self.player1.left
        or_right = self.player1.right

        # Choose hand
        hand = self.super_input(["left", "right"], "Player1 action hand:")
        # Choose action
        action = self.super_input(["act", "add"], f"Use {hand} to:")

        # if action == "add"
        if action == "add":
            # Choose who to add
            if_self = self.super_input(["yes", "no"], "If add to yourself:")

            if if_self == "yes":
                finger_add(self.player1, hand)
            else:
                # Choose which hand to add
                hand2 = self.super_input(["left", "right"], f"Add {hand} with player2's:")
                finger_add(self.player1, hand, self.player2, hand2)

            # detect shield
            detect_shield(or_left, or_right, self.player1)
            return "normal"

        # if action == "act":
        else:
            result = self.player1.use_weapon(self.player2, hand)
            detect_shield(or_left, or_right, self.player1)
            return result

    def a_step_player2(self):
        or_left = self.player2.left
        or_right = self.player2.right

        # Choose hand
        hand = self.super_input(["left", "right"], "Player2 action hand:")
        # Choose action
        action = self.super_input(["act", "add"], f"Use {hand} to:")

        # if action == "add"
        if action == "add":
            # Choose who to add
            if_self = self.super_input(["yes", "no"], "If add to yourself:")

            if if_self == "yes":
                finger_add(self.player2, hand)
            else:
                # Choose which hand to add
                hand2 = self.super_input(["left", "right"], f"Add {hand} with player1's:")
                finger_add(self.player2, hand, self.player1, hand2)

            # detect shield
            detect_shield(or_left, or_right, self.player2)
            return "normal"

        # if action == "act":
        else:
            result = self.player2.use_weapon(self.player1, hand)
            detect_shield(or_left, or_right, self.player2)
            return result

    def run_game(self):
        """Start game"""
        while True:
            # Player1's round
            while True:
                result = self.a_step_player1()
                if result == "pause" or result == "error":
                    continue
                else:
                    break

            if self.is_dead():
                break

            # Player2's round
            while True:
                result = self.a_step_player2()
                if result == "pause" or result == "error":
                    continue
                else:
                    break
            if self.is_dead():
                break


if __name__ == '__main__':
    game = FingerGame()
    game.run_game()
