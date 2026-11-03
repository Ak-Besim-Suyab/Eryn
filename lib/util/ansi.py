from enum import IntEnum

class AnsiColor(IntEnum):
    NONE = 0
    GRAY = 30
    RED = 31
    GREEN = 32
    GOLD = 33 
    BLUE = 34
    PINK = 35
    CYAN = 36
    WHITE = 37

class AnsiBgColor(IntEnum):
    NONE = 0
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PINK = 45
    CYAN = 46
    WHITE = 47

class AnsiFormat(IntEnum):
    NORMAL = 0
    BOLD = 1
    UNDERLINE = 4

class ANSI:
    def __init__(self, text: str):
        self._text = text
        self._color = AnsiColor.NONE
        self._bg_color = AnsiBgColor.NONE
        self._format = AnsiFormat.NORMAL

    def gray(self): self._color = AnsiColor.GRAY; return self
    def red(self): self._color = AnsiColor.RED; return self
    def green(self): self._color = AnsiColor.GREEN; return self
    def gold(self): self._color = AnsiColor.GOLD; return self
    def blue(self): self._color = AnsiColor.BLUE; return self
    def pink(self): self._color = AnsiColor.PINK; return self
    def cyan(self): self._color = AnsiColor.CYAN; return self
    def white(self): self._color = AnsiColor.WHITE; return self

    def bg_black(self): self._bg_color = AnsiBgColor.BLACK; return self
    def bg_red(self): self._bg_color = AnsiBgColor.RED; return self
    def bg_green(self): self._bg_color = AnsiBgColor.GREEN; return self
    def bg_yellow(self): self._bg_color = AnsiBgColor.YELLOW; return self
    def bg_blue(self): self._bg_color = AnsiBgColor.BLUE; return self
    def bg_pink(self): self._bg_color = AnsiBgColor.PINK; return self
    def bg_cyan(self): self._bg_color = AnsiBgColor.CYAN; return self
    def bg_white(self): self._bg_color = AnsiBgColor.WHITE; return self

    def bold(self): self._format = AnsiFormat.BOLD; return self
    def underline(self): self._format = AnsiFormat.UNDERLINE; return self

    def __str__(self):
        """將設定自動組合成 \u001b[{format};{fg};{bg}m 的格式"""
        codes = [str(self._format.value)]

        if self._color != AnsiColor.NONE:
            codes.append(str(self._color.value))

        if self._bg_color != AnsiBgColor.NONE:
            codes.append(str(self._bg_color.value))

        if len(codes) == 1 and codes[0] == "0":
            return self._text

        code_str = ";".join(codes)
        return f"\u001b[{code_str}m{self._text}\u001b[0m"

def wrap_ansi(text: str) -> str:
    """將文字包裝進 Discord 的 ansi 程式碼區塊中"""
    return f"```ansi\n{text}\n```"