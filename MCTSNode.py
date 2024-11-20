import math
import random
import aisrc
from fingergame import FingerGame
from settings import Setting


class MCTSNode:
    def __init__(self, state: FingerGame, parent=None, move=None, self_id=None):
        self.setting = Setting()
        self.state = state
        self.parent = parent
        self.move = move
        self.children = {}
        self.visits = 0.1
        self.wins = 0
        self.player = self.state.player1 if self_id == 1 else self.state.player2
        self.player2 = self.state.player2 if self_id == 1 else self.state.player1

    def get_possible_moves(self, change_player=None):
        # my_id = self.get_id()
        if change_player:
            my_id = self.player2
        else:
            my_id = self.player
        if my_id.left > 5 or my_id.left == 0:
            if my_id.left == 9:
                left_possible_move = \
                    [["left", "add", "yes"], ["left", "add", "no", "left"], ["left", "add", "no", "right"],
                     ["left", "act", "left"], ["left", "act", "right"]]
            else:
                left_possible_move = \
                    [["left", "add", "yes"], ["left", "add", "no", "left"], ["left", "add", "no", "right"],
                     ["left", "act"], ["left", "act"]]
        else:
            left_possible_move = \
                [["left", "add", "yes"], ["left", "add", "no", "left"], ["left", "add", "no", "right"]]

        if my_id.right > 5 or my_id.right == 0:
            if my_id.right == 9:
                right_possible_move = \
                    [["right", "add", "yes"], ["right", "add", "no", "left"], ["right", "add", "no", "right"],
                     ["right", "act", "left"], ["right", "act", "right"]]
            else:
                right_possible_move = \
                    [["right", "add", "yes"], ["right", "add", "no", "left"], ["right", "add", "no", "right"],
                     ["right", "act"], ["right", "act"]]
        else:
            right_possible_move = \
                [["right", "add", "yes"], ["right", "add", "no", "left"], ["right", "add", "no", "right"]]

        return left_possible_move + right_possible_move

    def is_fully_expanded(self):
        return len(self.children) == len(self.get_possible_moves())

    def best_child(self, exploration_weight="none"):
        if type(exploration_weight) == str:
            exploration_weight = \
                random.randint(int((1 - self.setting.exp_w_distribution) * self.setting.exploration_weight),
                               int((1 + self.setting.exp_w_distribution) * self.setting.exploration_weight + 1))
        return max(self.children.values(), key=lambda c: c.wins / c.visits + exploration_weight * math.sqrt(
            (2 * math.log(self.visits) / c.visits)))

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
        state = self.state
        best_score = 0
        worst_score = 0
        simu_time = 0
        while not self.state.is_dead():
            simu_time += 1
            if simu_time > self.setting.simulate_depth:
                break

            if state.current_player == self.player:
                # move = random.choice(self.get_possible_moves())
                best_move = None
                for move in self.get_possible_moves():
                    next_state = aisrc.copy_state(self.state)
                    next_state.current_player.take_step(next_state.waiting_player, move)
                    winner = next_state.is_dead()
                    if winner == self.player:
                        best_move = move
                        break
                    # elif winner == self.player2:
                    else:
                        best_score, worst_score = aisrc.score(self, simu_time, best_score, worst_score)
                        best_move = move

                move = best_move if best_move else self.best_child().move
                # random.choice(self.get_possible_moves())

            else:
                # Assuming perfect opponent for player2
                best_move = None
                for move in self.get_possible_moves(change_player=True):
                    next_state = aisrc.copy_state(self.state)
                    next_state.waiting_player.take_step(next_state.current_player, move)
                    winner = next_state.is_dead()
                    if winner == self.player2:
                        best_move = move
                        break
                    # elif winner == self.player2:
                    else:
                        best_score, worst_score = aisrc.score(self, simu_time, best_score, worst_score)
                        best_move = move
                move = best_move

            state.make_move(move)

        winner = state.is_dead()
        if winner:
            return (simu_time, "1") if winner == self.state.player1 else (simu_time, "2")
        else:
            return simu_time, self.setting.best_award * best_score - self.setting.worst_punish * worst_score
