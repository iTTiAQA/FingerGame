import math
import time
import random
import aisrc
from fingergame import FingerGame
from settings import Setting


"""Basic adding movements: ["add", "yes/no", "left/right"]"""
"""Basic acting movements: ["act", "left/right", "left/right"]"""


class MCTSNode:
    def __init__(self, state: FingerGame, parent=None, move=None, self_id=None):
        self.setting = Setting()
        self.state = state
        self.parent = parent
        self.move = move
        self.children = {}
        self.visits = 0
        self.wins = 0
        self.player = self.state.player1 if self_id == 1 else self.state.player2
        self.player2 = self.state.player2 if self_id == 1 else self.state.player1

    def get_id(self):
        return self.player

    """
    def get_possible_moves(self):
        my_id = self.get_id()
        if my_id.left > 5 or my_id.right > 5:
            if my_id.left == 9 or my_id.right == 9:
                # able to use hook
                return [["left", "add", "yes"], ["right", "add", "yes"],
                        ["left", "add", "no", "left"], ["right", "add", "no", "left"],
                        ["left", "add", "no", "right"], ["right", "add", "no", "right"],
                        ["left", "act", "left"], ["left", "act", "right"],
                        ["right", "act", "left"], ["right", "act", "right"]]
            else:
                # able to use others
                return [["left", "add", "yes"], ["right", "add", "yes"],
                        ["left", "add", "no", "left"], ["right", "add", "no", "left"],
                        ["left", "add", "no", "right"], ["right", "add", "no", "right"],
                        ["act", "left"], ["act", "right"]]
        else:
            # only able to add
            return [["left", "add", "yes"], ["right", "add", "yes"],
                    ["left", "add", "no", "left"], ["right", "add", "no", "left"],
                    ["left", "add", "no", "right"], ["right", "add", "no", "right"]]
    """

    def get_possible_moves(self):
        my_id = self.get_id()
        move = []
        if my_id.left > 5:
            if my_id.left == 9:
                left_possible_move = \
                    [["left", "add", "yes"],  ["left", "add", "no", "left"], ["left", "add", "no", "right"],
                     ["left", "act", "left"], ["left", "act", "right"]]
            else:
                left_possible_move = \
                    [["left", "add", "yes"], ["left", "add", "no", "left"], ["left", "add", "no", "right"],
                     ["left", "act"], ["left", "act"]]
        else:
            left_possible_move = \
                [["left", "add", "yes"], ["left", "add", "no", "left"], ["left", "add", "no", "right"]]

        if my_id.right > 5:
            if my_id.right == 9:
                right_possible_move = \
                    [["right", "add", "yes"],  ["right", "add", "no", "left"], ["right", "add", "no", "right"],
                     ["right", "act", "left"], ["right", "act", "right"]]
            else:
                right_possible_move = \
                    [["right", "add", "yes"], ["right", "add", "no", "left"], ["right", "add", "no", "right"],
                     ["right", "act"], ["right", "act"]]
        else:
            right_possible_move = \
                [["right", "add", "yes"], ["right", "add", "no", "left"], ["right", "add", "no", "right"]]
        for value in left_possible_move:
            move.append(value)
        for value in right_possible_move:
            move.append(value)
        return move

    def is_fully_expanded(self):
        return len(self.children) == len(self.get_possible_moves())

    def best_child(self, exploration_weight=1.41):
        return max(self.children.values(), key=lambda c: c.wins / c.visits + exploration_weight * math.sqrt(
            (2 * math.log(self.visits) / c.visits)))

    # @aisrc.print_round
    def expand(self):
        if self.is_fully_expanded():
            return None
        move = random.choice(self.get_possible_moves())
        next_state = aisrc.copy_state(self.state)
        result = next_state.current_player.take_step(next_state.waiting_player, move)
        if result != "pause":
            next_state.change_term()
        child = MCTSNode(next_state, self, move)
        self.children[tuple(move)] = child
        return child

    def simulate(self):
        start_time = time.perf_counter()
        state = self.state
        best_score = 0
        worst_score = 0
        while not self.state.is_dead():
            current_time = time.perf_counter()
            if current_time - start_time > self.setting.cut_time:
                break

            if state.current_player == self:
                move = random.choice(self.get_possible_moves())
            else:
                # Assuming perfect opponent for player2
                # best_score = float('-inf')
                best_move = None
                for move in self.get_possible_moves():
                    next_state = aisrc.copy_state(self.state)
                    next_state.waiting_player.take_step(next_state.current_player, move)
                    winner = next_state.is_dead()
                    if winner == self.player:
                        # best_score = float('inf')
                        best_move = move
                        break
                    # elif score == self.player:
                    else:
                        best_score = max(self.player.HP-self.player2.HP, best_score)
                        worst_score = min(self.player2.HP-self.player.HP, worst_score)
                        best_move = move
                move = best_move
            state.make_move(move)
        winner = None
        winner = state.is_dead()
        if winner:
            return "1" if winner == self.state.player1 else "2"
        else:
            return self.setting.best_award * best_score - self.setting.worst_punish * worst_score
