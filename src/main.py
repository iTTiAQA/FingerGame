from core import FingerGame
from AddOns.ui import UI
from AddOns.ai import AI

game = FingerGame()
UI = UI()
AI = AI()


print("Welcome to Finger Game!")
gamemode = input("Please select a game mode: \na: AI vs AI, \nb: AI vs Player, \nc: Player vs AI, \nd: Player vs Player\n: ")

result = game.tick0()
UI.display(result)
while True:
    while True:
        if gamemode == "c" or gamemode == "d":
            action = UI.get_action()
        else:
            action = AI.get_action(result)
        result = game.tick(action)
        UI.display(result)
        if result["status"] == "normal":
            break
    while True:
        if gamemode == "a" or gamemode == "c":
            action = AI.get_action(result)
        else:
            action = UI.get_action()
        result = game.tick(action)
        UI.display(result)
        if result["status"] == "normal":
            break
