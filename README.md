# FingerGame

**FingerGame** 是一款基于 Python 的两人手指游戏。

## 程序入口: main.py

## 接口说明:

### action: str
```Python
"all": ["left", "add", "no", "left"],
"alr": ["left", "add", "no", "right"],
"arl": ["right", "add", "no", "left"],
"arr": ["right", "add", "no", "right"],
"als": ["left", "add", "yes"],
"ars": ["right", "add", "yes"],
"ul": ["left", "act"],
"ur": ["right", "act"],
"ull": ["left", "act", "left"],
"ulr": ["left", "act", "right"],
"url": ["right", "act", "left"],
"urr": ["right", "act", "right"]
```

### return: dict
```Python
{
    "status": "normal",
    "current_player": self.current_player.num,
    "waiting_player": self.waiting_player.num,
    "player1": {
        "left": self.player1.left,
        "right": self.player1.right,
        "HP": self.player1.HP,
        "shield": self.player1.shield
    },
    "player2": {
        "left": self.player2.left,
        "right": self.player2.right,
        "HP": self.player2.HP,
        "shield": self.player2.shield
    }
}

or

{
    "status": "game over",
    "winner": self.is_dead().num
}

or

{
    "status": "error",
    "msg": "invalid action"
}

```
