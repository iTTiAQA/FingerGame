from settings import Setting
from weapon import Weapon
from source import detect_shield
from source import finger_add


class Player:
    def __init__(self, game, num):
        self.game = game
        self.settings = Setting()
        self.HP = self.settings.initHP
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

    def use_weapon(self, player2, hand):
        if hand == "left":
            using_hand = self.left
        else:
            using_hand = self.right

        if 6 > using_hand > 0:
            return "error"

        elif using_hand == 6:
            self.weapon.bow(self, player2, hand)

        elif using_hand == 7:
            self.weapon.pause(self, hand)
            return "pause"

        elif using_hand == 8:
            self.weapon.gun(self, player2, hand)

        elif using_hand == 9:
            hand2 = self.super_input([self.settings.left_hand, self.settings.right_hand], "Hook hand:",
                                     f"Player2 Left:{player2.left}    Player2 Right:{player2.right}")
            hand2 = "left" if hand2 == self.settings.left_hand else "right"
            self.weapon.hook(self, player2, hand, hand2)

        elif using_hand == 0:
            self.weapon.hammer(self, player2, hand)

        else:
            return "error"

        return "normal"

    def take_step(self, player2, take_action=None):
        pre_left = self.left
        pre_right = self.right

        # Choose hand
        hand = self.super_input([self.settings.left_hand, self.settings.right_hand], f"Player{self.num} action hand:")
        hand = "left" if hand == self.settings.left_hand else "right"
        # Choose action
        action = self.super_input([self.settings.act, self.settings.add], f"Use {hand} to:")
        action = "act" if action == self.settings.act else "add"

        # if action == "add"
        if action == "add":
            # Choose who to add
            if_self = self.super_input([self.settings.yes, self.settings.no], "If add to yourself:")
            if_self = "yes" if if_self == self.settings.yes else "no"

            if if_self == "yes":
                finger_add(self, hand)
            else:
                # Choose which hand to add
                hand2 = self.super_input([self.settings.left_hand, self.settings.right_hand],
                                         f"Add {hand} with player{self.get_op_num()}'s:")
                hand2 = "left" if hand2 == self.settings.left_hand else "right"
                finger_add(self, hand, player2, hand2)

            # detect shield
            detect_shield(pre_left, pre_right, self)
            return "normal"

        # if action == "act":
        else:
            # use weapon
            result = self.use_weapon(player2, hand)
            # detect shield
            detect_shield(pre_left, pre_right, self)
            return result
