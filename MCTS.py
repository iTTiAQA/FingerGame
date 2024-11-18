from MCTSNode import MCTSNode
from fingergame import FingerGame


class MCTS:
    def __init__(self, state: FingerGame, input_id: int, iterations=1000):
        self.root = MCTSNode(state, self_id=input_id)
        self.iterations = iterations
        self.using_id = input_id
        # self.hash_list = {}

    def run(self):
        for _ in range(self.iterations):
            node = self.root
            state = node.state

            # Selection
            while not state.is_dead() and not node.is_fully_expanded():
                # node = node.best_child()
                node = node.expand()
                state = node.state

            # Expansion
            if not state.is_dead() and node.is_fully_expanded():
                # node = node.expand()
                node = node.best_child()
                # state = node.state

            # Simulation
            winner = node.simulate()

            # Backpropagation
            while node is not None:
                node.visits += 1
                # node.wins += result if node.state.current_player == node.state.player2 else -result
                # node.wins += 1 if winner == self.using_id else -1
                if type(winner) == str:
                    node.wins += 1 if int(winner) == self.using_id else -1
                else:
                    node.wins += winner
                node = node.parent

        return self.root.best_child()
