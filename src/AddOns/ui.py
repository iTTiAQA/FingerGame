import pprint


class UI:
    def display(self, dic: dict):
        if dic["status"] == "normal":
            print(f"当前是{dic['current_player']}的回合：")
            print(f"玩家1: 血量:{dic["player1"]["HP"]}  盾牌:{dic["player1"]["shield"]}  左手:{dic['player1']['left']}  右手:{dic['player1']['right']}")
            print(f"玩家2: 血量:{dic['player2']['HP']}  盾牌:{dic['player2']['shield']}  左手:{dic['player2']['left']}  右手:{dic['player2']['right']}")
        else:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(dic)
            exit()

    def get_action(self):
        action = input("请输入动作：")
        return action
