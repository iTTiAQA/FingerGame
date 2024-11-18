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
        self.iterations = 200      # Breadth correlate
        self.cut_time = 0.05       # Depth correlate

        self.exploration_weight = 1.21

        self.worst_punish = 0.00
        self.best_award = 0.05

        self.win_award = 5
