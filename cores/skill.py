import time

class Skill:
    """
    這是技能的抽象類別
    目前定義冷卻時間與使用者的時間戳記，以及判斷冷卻的方法
    """
    def __init__(self, skill_cooldown: float = 5.0):
        self.skill_cooldown = skill_cooldown
        self.skill_timestamps = {}

    def is_cooldown(self, player_id) -> tuple[bool, float]:
        now = time.time()
        if player_id in self.skill_timestamps:
            elapsed = now - self.skill_timestamps[player_id]
            if elapsed < self.skill_cooldown:
                remaining = self.skill_cooldown - elapsed
                return True, remaining
            
        self.skill_timestamps[player_id] = now
        return False, 0.0