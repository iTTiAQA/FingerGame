def count_five(num1, num2):
    """Used for counting shield in fun: detect_shield()"""
    if num1 == 5 and num2 == 5:
        return 2
    elif num1 == 5 or num2 == 5:
        return 1
    else:
        return 0


def detect_shield(pre_left, pre_right, player):
    """Used for counting shield after a step"""
    gen_shield = count_five(player.left, player.right) - count_five(pre_left, pre_right)
    if gen_shield > 0:
        player.shield += 5 * gen_shield
    else:
        cur_shield = 5 * count_five(player.left, player.right)
        if player.shield > cur_shield:
            player.shield = cur_shield


def finger_add(player1, hand1, player2=None, hand2=None):
    """Used for add fingers"""
    # if add to another player
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

    # Make a reasonable range
    player1.left %= 10
    player1.right %= 10


class Weapon:
    def __init__(self):
        pass

    def attack(self, player2, hurt):
        if player2.shield > hurt:
            player2.shield -= hurt
        else:
            player2.HP -= hurt - player2.shield
            player2.shield = 0

    def shield(self):
        pass

    def bow(self, player1, player2, hand):
        if hand == "left":
            hurt = player1.right * 0.5
        else:
            hurt = player1.left * 0.5

        self.attack(player2, hurt)
        player1.left = 1
        player1.right = 1

    def gun(self, player1, player2, hand):
        if hand == "left":
            hurt = player1.right
        else:
            hurt = player1.left

        self.attack(player2, hurt)
        player1.left = 1
        player1.right = 1

    def adder(self, player1, player2, hand1, hand2):

        if hand2 == "left":
            player2.left += 7
            player2.left %= 10
        else:
            player2.right += 7
            player2.right %= 10

        if hand1 == "left":
            player1.left = 1
        else:
            player1.right = 1

    def hook(self, player1, player2, hand1, hand2):

        if hand2 == "left":
            temp2 = player2.left
        else:
            temp2 = player2.right

        if hand1 == "left":
            player1.left = temp2
        else:
            player1.right = temp2

        if hand2 == "left":
            player2.left = 1
        else:
            player2.right = 1

    def hammer(self, player1, player2, hand):
        if hand == "left":
            player1.left = 1
        else:
            player1.right = 1

        if player2.shield > 0:
            player2.shield = 0
        else:
            player2.HP -= 2


class Player:
    def __init__(self, game, num):
        self.game = game
        self.HP = 5
        self.left = 1
        self.right = 1
        self.shield = 0
        self.weapon = Weapon()
        self.num = num
        self.get_op_num()

    def get_op_num(self):
        if self.num == 1:
            return 2
        else:
            return 1

    def super_input(self, choice, string, print_string=None):
        """To simplify the input code"""
        while True:
            self.game.display()
            if print_string:
                print(print_string)
            _input = input(string)
            if _input in choice:
                return _input

    def use_weapon(self, player2, hand, hand2=None):
        if hand == "left":
            using_hand = self.left
        else:
            using_hand = self.right

        if 6 > using_hand > 0:
            return "error"

        elif using_hand == 6:
            self.weapon.bow(self, player2, hand)

        elif using_hand == 7:
            self.weapon.adder(self, player2, hand, hand2)

        elif using_hand == 8:
            self.weapon.gun(self, player2, hand)

        elif using_hand == 9:
            self.weapon.hook(self, player2, hand, hand2)

        elif using_hand == 0:
            self.weapon.hammer(self, player2, hand)

        else:
            return "error"

        return "normal"

    def take_step(self, player2, action):
        """action: all, alr, arl, arr, als, ars, ul, ur, ull, ulr, url, urr"""
        choices = {"all": ["left", "add", "no", "left"], "alr": ["left", "add", "no", "right"], "arl": ["right", "add", "no", "left"], "arr": ["right", "add", "no", "right"], "als": ["left", "add", "yes"], "ars": ["right", "add", "yes"], "ul": ["left", "act"], "ur": ["right", "act"], "ull": ["left", "act", "left"], "ulr": ["left", "act", "right"], "url": ["right", "act", "left"], "urr": ["right", "act", "right"]}
        take_action = choices[action]

        pre_left = self.left
        pre_right = self.right

        # Choose hand:
        # hand = self.super_input(["left", "right"], f"Player{self.num} action hand:")
        hand = take_action[0]

        # Choose action:
        # action = self.super_input(["act", "add"], f"Use {hand} to:")
        action = take_action[1]

        # if action == "add"
        if action == "add":
            # Choose who to add:
            # if_self = self.super_input(["yes", "no"], "If add to yourself:")
            if_self = take_action[2]

            if if_self == "yes":
                finger_add(self, hand)
            else:
                # Choose which hand to add:
                # hand2 = self.super_input(["left", "right"], f"Add {hand} with player{self.get_op_num()}'s:")
                hand2 = take_action[3]
                finger_add(self, hand, player2, hand2)

            # detect shield
            detect_shield(pre_left, pre_right, self)
            return "normal"

        # if action == "act":
        else:
            # use weapon
            get_len = len(take_action)
            hook_hand = None
            if get_len == 3:
                hook_hand = take_action[2]
            result = self.use_weapon(player2, hand, hook_hand)
            # detect shield
            detect_shield(pre_left, pre_right, self)
            return result


class FingerGame:
    """Class for game action and resources"""

    def __init__(self):
        self.player1 = Player(self, 1)
        self.player2 = Player(self, 2)
        self.current_player = self.player1
        self.waiting_player = self.player2

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

    def tick0(self) -> dict:
        return {"status": "normal", "current_player": self.current_player.num, "waiting_player": self.waiting_player.num, "player1": {"left": self.player1.left, "right": self.player1.right, "HP": self.player1.HP, "shield": self.player1.shield}, "player2": {"left": self.player2.left, "right": self.player2.right, "HP": self.player2.HP, "shield": self.player2.shield}}

    def tick(self, action) -> dict:
        result = self.current_player.take_step(self.waiting_player, action)
        if self.is_dead():
            return {"status": "game over", "winner": self.is_dead().num}
        if result != "error":
            self.current_player, self.waiting_player = self.waiting_player, self.current_player
            return {"status": "normal", "current_player": self.current_player.num, "waiting_player": self.waiting_player.num, "player1": {"left": self.player1.left, "right": self.player1.right, "HP": self.player1.HP, "shield": self.player1.shield}, "player2": {"left": self.player2.left, "right": self.player2.right, "HP": self.player2.HP, "shield": self.player2.shield}}
        else:
            return {"status": "error", "msg": "invalid action"}


if __name__ == "__main__":
    game = FingerGame()
    while True:
        print(game.tick(input("input:")))
