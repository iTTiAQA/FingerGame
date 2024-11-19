class Setting:
    def __init__(self):
        # player settings:
        self.initHP = 5

        # input settings:
        self.left_hand = "left"
        self.right_hand = "right"
        self.act = "act"
        self.add = "add"
        self.yes = "yes"
        self.no = "no"

        # MCTS settings:
        self.iterations = 5000      # Breadth correlate
        self.simulate_depth = 8       # Depth correlate

        self.exploration_weight = 45
        self.exp_w_distribution = 0.2

        self.worst_punish = 0.10
        self.best_award = 0.25

        self.win_award = 7
        self.loss_punish = 5
