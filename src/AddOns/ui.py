import enum
import os


class CTKey(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    RIGHT = enum.auto()
    LEFT = enum.auto()
    ESC = enum.auto()
    ENTER = enum.auto()
    DELETE = enum.auto()
    BACK = enum.auto()
    TAB = enum.auto()


def getch() -> CTKey | str:
    pass


def init_term() -> None:
    global getch, clear_screen

    import sys

    if sys.platform.startswith("win"):
        import msvcrt

        # Overwrite global function "getch"
        def getch() -> CTKey | str:
            key = msvcrt.getch()
            try:
                s = key.decode()
                if ord(s) == 27:
                    return CTKey.ESC
                elif ord(s) == 13:
                    return CTKey.ENTER
                elif ord(s) == 9:
                    return CTKey.TAB
                elif ord(s) == 8:
                    return CTKey.BACK
                else:
                    return s
            except UnicodeDecodeError:
                key = key + msvcrt.getch()
                if key == b"\x00\x07":
                    return CTKey.ESC
                s = key.decode("gbk")
                if s == "郒":
                    return CTKey.UP
                elif s == "郟":
                    return CTKey.DOWN
                elif s == "郖":
                    return CTKey.LEFT
                elif s == "郙":
                    return CTKey.RIGHT
                elif s == "郤":
                    return CTKey.DELETE
                else:
                    return s

        def clear_screen() -> None:
            os.system("cls")

    elif sys.platform.startswith("linux"):
        import functools
        import selectors
        import termios
        import tty

        sel: selectors.DefaultSelector = selectors.DefaultSelector()
        sel.register(sys.stdin, selectors.EVENT_READ)

        old_attr = termios.tcgetattr(sys.stdin)

        def _getch_impl() -> CTKey | bytes:
            key: bytes = sys.stdin.buffer.raw.read(1)
            if key == b"\n":
                return CTKey.ENTER
            elif key == b"\t":
                return CTKey.TAB
            elif (key_code := ord(key)) == 127:
                return CTKey.BACK
            elif key_code == 27:
                if not sel.select(0):
                    return CTKey.ESC
                ch = sys.stdin.buffer.raw.read(1)
                if ch != b"[":
                    return ch
                else:
                    ch2 = sys.stdin.buffer.raw.read(1)
                    if ch2 == b"A":
                        return CTKey.UP
                    elif ch2 == b"B":
                        return CTKey.DOWN
                    elif ch2 == b"C":
                        return CTKey.RIGHT
                    elif ch2 == b"D":
                        return CTKey.LEFT
                    elif ch2 == b"3" and sys.stdin.buffer.raw.read(1) == b"~":
                        return CTKey.DELETE
                    else:
                        return ch2
            else:
                return key

        def clear_screen() -> None:
            os.system("clear")

        # Overwrite global function "getch"
        @functools.wraps(_getch_impl)
        def getch() -> CTKey | str:
            tty.setcbreak(sys.stdin)
            ret = _getch_impl()
            termios.tcsetattr(sys.stdin, termios.TCSANOW, old_attr)
            return ret.decode() if isinstance(ret, bytes) else ret

    else:
        assert False, "Unsupported operating system"


init_term()


"""dic = {
    "status": "normal",
    "current_player": {
        "num": self.current_player.num,
        "left": self.player1.left,
        "right": self.player1.right,
        "HP": self.player1.HP,
        "shield": self.player1.shield
    },
    "waiting_player": {
        "num": self.waiting_player.num,
        "left": self.player2.left,
        "right": self.player2.right,
        "HP": self.player2.HP,
        "shield": self.player2.shield
    },
    "history": {
        "action": action,
        "old_state": {
                        "current_player": {
                            "num": self.current_player.num,
                            "left": self.player1.left,
                            "right": self.player1.right,
                            "HP": self.player1.HP,
                            "shield": self.player1.shield
                        },
                        "waiting_player": {
                            "num": self.waiting_player.num,
                            "left": self.player2.left,
                            "right": self.player2.right,
                            "HP": self.player2.HP,
                            "shield": self.player2.shield
                        }
                    }
    }
}"""


class UI:
    def display(self, dic: dict):
        clear_screen()
        if dic["status"] == "normal":
            print(f"  玩家{dic['waiting_player']['num']}: 血量:{dic['waiting_player']['HP']}  盾牌:{dic['waiting_player']['shield']} 左手:{dic['waiting_player']['left']}  右手{dic["current_player"]["right"]}")
            print(f"\n->玩家{dic['current_player']['num']}: 血量:{dic['current_player']['HP']}  盾牌:{dic['current_player']['shield']} 左手:{dic['current_player']['left']}  右手{dic["current_player"]["right"]}")
        elif dic["status"] == "game over":
            print(f"游戏结束！玩家{dic['winner']}获胜！")
            exit()
        elif dic["status"] == "error":
            print("错误的输入！请重新输入！")

    def getchoice(self, choices: list):
        while True:
            _i = getch()
            if _i in choices:
                return _i

    def get_action(self):
        print("选择你的动作:[u:act/a:add]")
        act = self.getchoice(["u", "a"])
        print("选择你要操作的手:[l:left/r:right]")
        myhand = self.getchoice(["l", "r"])
        print("选择对象:[l:left/r:right/s:self/[space]:None]")
        obj = self.getchoice(["l", "r", "s", " "])
        if obj == " ":
            obj = ""
        action = act + myhand + obj
        return action
