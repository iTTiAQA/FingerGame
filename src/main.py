from core import FingerGame
from AddOns.ui import UI
from AddOns.ai import AI

game = FingerGame()
UI = UI()
AI = AI()

UI.display(game.tick0())
while True:
    while True:
        action = UI.get_action()
        result = game.tick(action)
        UI.display(result)
        if result["status"] == "normal":
            break
    while True:
        action = AI.get_action(result)
        result = game.tick(action)
        UI.display(result)
        if result["status"] == "normal":
            break
