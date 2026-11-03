"""雜項物件與函式
"""

class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"