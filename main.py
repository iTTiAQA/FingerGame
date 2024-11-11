from player import Player


def count_five(num1, num2):
    """Used for counting shield in fun: detect_shield()"""
    if num1 == 5 and num2 == 5:
        return 2
    elif num1 == 5 or num2 == 5:
        return 1
    else:
        return 0


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

    def detect_shield(self, or_left, or_right, player):
        """Used for counting shield after a step"""
        gen_shield = count_five(player.left, player.right) - count_five(or_left, or_right)
        if gen_shield > 0:
            player.shield += 5*gen_shield
        else:
            cur_shield = 5*count_five(player.left, player.right)
            if player.shield > cur_shield:
                player.shield = cur_shield
            else:
                pass

    def is_dead(self):
        if self.player1.HP <= 0 or self.player2.HP <= 0:
            return True

    def _add(self, player1, hand1, player2=None, hand2=None):
        if player2:
            if hand1 == "left":
                if hand2 == "left":
                    player1.left += player2.left
                else:
                    player1.left += player2.right
            # if hand1 == "right":
            else:
                if hand2 == "left":
                    player1.right += player2.left
                else:
                    player1.right += player2.right

        # if add to self
        else:
            if hand1 == "left":
                player1.left += player1.right
            else:
                player1.right += player1.left

        player1.left %= 10
        player1.right %= 10

    def a_step_player1(self):
        or_left = self.player1.left
        or_right = self.player1.right

        # Choose hand
        while True:
            self.display()
            hand = input("Player1 action hand:")
            if hand == "left" or hand == "right":
                break

        # Choose action
        while True:
            self.display()
            action = input(f"Use {hand} to:")
            if action == "act" or action == "add":
                break

        # if action == "add"
        if action == "add":

            # Choose who to add
            while True:
                self.display()
                if_self = input("If add to yourself:")
                if if_self == "yes" or if_self == "no":
                    break
            if if_self == "yes":
                self._add(self.player1, hand)

            else:
                # Choose which hand to add
                while True:
                    self.display()
                    hand2 = input(f"Add {hand} with player2's:")
                    if hand2 == "left" or hand2 == "right":
                        break
                self._add(self.player1, hand, self.player2, hand2)

            self.detect_shield(or_left, or_right, self.player1)
            return "normal"

        # if action == "act":
        else:
            result = self.player1.use_weapon(self.player2, hand)
            self.detect_shield(or_left, or_right, self.player1)
            return result

    def a_step_player2(self):
        or_left = self.player2.left
        or_right = self.player2.right

        # Choose hand
        while True:
            self.display()
            hand = input("Player2 action hand:")
            if hand == "left" or hand == "right":
                break

        # Choose action
        while True:
            self.display()
            action = input(f"Use {hand} to:")
            if action == "act" or action == "add":
                break

        # if action == "add"
        if action == "add":

            # Choose who to add
            while True:
                self.display()
                if_self = input("If add to yourself:")
                if if_self == "yes" or if_self == "no":
                    break
            if if_self == "yes":
                self._add(self.player2, hand)

            else:
                # Choose which hand to add
                while True:
                    self.display()
                    hand2 = input(f"Add {hand} with player1's:")
                    if hand2 == "left" or hand2 == "right":
                        break

                self._add(self.player2, hand, self.player1, hand2)

            self.detect_shield(or_left, or_right, self.player2)
            return "normal"

        # if action == "act":
        else:
            result = self.player2.use_weapon(self.player1, hand)
            self.detect_shield(or_left, or_right, self.player2)
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
