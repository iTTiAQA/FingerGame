from fingergame import FingerGame
import math


def set_state(state_list: list, if_not_2ai=False):
    if if_not_2ai:
        state = FingerGame(state_list[9][0], state_list[9][1])
    else:
        state = FingerGame(if_ai1=1, if_ai2=1)
    state.player1.HP = state_list[0]
    state.player1.shield = state_list[1]
    state.player1.left = state_list[2]
    state.player1.right = state_list[3]
    state.player2.HP = state_list[4]
    state.player2.shield = state_list[5]
    state.player2.left = state_list[6]
    state.player2.right = state_list[7]
    state.current_player = state.player1 if state_list[8] else state.player2
    state.waiting_player = state.player2 if state_list[8] else state.player1

    return state


def get_state(state: FingerGame):
    state_list = [0 for _ in range(10)]
    state_list[0] = state.player1.HP
    state_list[1] = state.player1.shield
    state_list[2] = state.player1.left
    state_list[3] = state.player1.right
    state_list[4] = state.player2.HP
    state_list[5] = state.player2.shield
    state_list[6] = state.player2.left
    state_list[7] = state.player2.right
    state_list[8] = 1 if state.current_player == state.player1 else 0
    state_list[9] = state.if_ai

    return state_list


def copy_state(state: FingerGame, if_not_2ai=False):
    return set_state(get_state(state), if_not_2ai)


def sigmoid(x: float):
    return 1/(1+math.exp(-x))


def score(node, simu_time, best_score, worst_score):
    best_decay = sigmoid(0.5 * node.setting.simulate_depth - simu_time - 1)
    worst_decay = sigmoid(0.5 * node.setting.simulate_depth - simu_time + 2)
    best_score = max(best_decay * (node.setting.initHP / 2 * (node.player2.HP + 1)), best_score)
    worst_score = max(worst_decay * (node.setting.initHP / 2 * (node.player.HP + 1)), worst_score)
    return best_score, worst_score
