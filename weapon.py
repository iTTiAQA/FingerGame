class Weapon:
    def __init__(self):
        pass

    def attack(self, player2, hurt):
        if player2.shield > hurt:
            player2.shield -= hurt
        else:
            player2.HP -= hurt-player2.shield
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

    def pause(self, player1, hand):
        if hand == "left":
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
            player2.HP -= 3
