from source import detect_shield
from source import finger_add
from player import Player


class AiPlayer(Player):
    def __init__(self, game, num):
        super().__init__(game, num)

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
            self.weapon.pause(self, hand)
            return "pause"

        elif using_hand == 8:
            self.weapon.gun(self, player2, hand)

        elif using_hand == 9:
            self.weapon.hook(self, player2, hand, hand2)

        elif using_hand == 0:
            self.weapon.hammer(self, player2, hand)

        else:
            return "error"

        return "normal"

    def take_step(self, player2, take_action=None):
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
            if get_len == 4:
                hook_hand = take_action[3]
            result = self.use_weapon(player2, hand, hook_hand)
            # detect shield
            detect_shield(pre_left, pre_right, self)
            return result
