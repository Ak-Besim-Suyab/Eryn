"""
這裡是技能 (指令) 的抽象類別，定義冷卻時間與使用者的時間戳記
"""

class Action:
    def __init__(self):
        self.timestamps: dict = {}