from settings import Setting
from weapon import Weapon


class Player:
    def __init__(self):
        self.settings = Setting()
        self.HP = self.settings.initHP
        self.left = 1
        self.right = 1
        self.shield = self.settings.init_shield
        self.weapon = Weapon()

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
            while True:
                print(f"Player2 Left:{player2.left}    Player2 Right:{player2.right}")
                hand2 = input("Hook hand:")
                if hand2 == "left" or hand2 == "right":
                    break
            self.weapon.hook(self, player2, hand, hand2)

        elif using_hand == 0:
            self.weapon.hammer(self, player2, hand)

        else:
            return "error"

        return "normal"
