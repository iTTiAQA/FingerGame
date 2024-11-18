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


def super_input(choice, string, print_string=None):
    """To simplify the input code"""
    while True:
        if print_string:
            print(print_string)
        _input = input(string)
        if _input in choice:
            return _input
