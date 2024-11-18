class Setting:
    def __init__(self):
        # player settings:
        self.initHP = 5

        # MCTS settings:
        self.iterations = 1000      # Breath correlate
        self.cut_time = 0.5        # Depth correlate

        self.worst_punish = 0.005
        self.best_award = 0.01
