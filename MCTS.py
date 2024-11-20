from MCTSNode import MCTSNode
from fingergame import FingerGame
from settings import Setting


class MCTS:
    def __init__(self, state: FingerGame, input_id: int, iterations=1000):
        self.setting = Setting()
        self.root = MCTSNode(state, self_id=input_id)
        self.iterations = iterations
        self.using_id = input_id

    def run(self):
        for _ in range(self.iterations):
            node = self.root
            state = node.state

            # Selection
            while not state.is_dead() and not node.is_fully_expanded():
                node = node.expand()
                state = node.state

            # Expansion
            if not state.is_dead() and node.is_fully_expanded():
                node = node.best_child()

            # Simulation
            winner = node.simulate()

            # Backpropagation
            while node is not None:
                node.visits += 1
                if type(winner) == str:
                    node.wins += self.setting.win_award if int(winner) == self.using_id else -self.setting.win_award
                else:
                    node.wins += winner
                node = node.parent

        return self.root.best_child(exploration_weight=0)
