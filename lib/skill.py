from models import Skill

def get(player: int, name: str) -> Skill:
    skill, _ = Skill.get_or_create(player=player, name=name)
    return skill

def add_experience(player: int, name: str, amount: float):
    """
    增加玩家技能經驗, `player`為玩家`id`,`name`為技能名稱,`amount`為要增加的數量
    """
    if not _valid(name, amount):
        return

    Skill.get_or_create(player=player, name=name)

    (Skill
     .update(experience = Skill.experience + amount)
     .where(Skill.player == player)
     .where(Skill.name == name)
     .execute())

def _valid(name: str, amount: float) -> bool:

    if amount < 0:
        return False
    
    return True