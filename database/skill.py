from peewee import *
from database.generic import db
from database.player import Player


class Skill(Model):
    # associated skills in Player.skills
    player = ForeignKeyField(Player, backref='skills', on_delete='CASCADE')

    name = TextField()
    level = IntegerField(default = 1)
    exp = IntegerField(default = 0)

    class Meta:
        database = db
        indexes = (
            (('player', 'name'), True),
        )
    
    @classmethod
    def get_or_create_skill(cls, player_id: int, skill_name: str):
        skill, created = cls.get_or_create(
            player_id = player_id,
            name = skill_name
        )
        return skill
    
    @classmethod
    def add_experience(cls, player_id: int, amount: int, skill_name: str) -> dict:
        skill = cls.get_or_create_skill(player_id, skill_name)
        
        skill.exp += amount
        
        old_level = skill.level
        new_levels = []
        
        # 使用 while 循環處理連續升級的情況
        while skill.exp >= cls._get_required_exp(skill.level):
            # 扣除本級所需的經驗
            skill.exp -= cls._get_required_exp(skill.level)
            # 升級
            skill.level += 1
            new_levels.append(skill.level)
        
        # 保存到數據庫
        skill.save()
        
        # 返回結果字典
        return {
            'level': skill.level,
            'exp': skill.exp,
            'leveled_up': skill.level > old_level,
            'new_levels': new_levels
        }
    
    @staticmethod
    def _get_required_exp(level: int) -> int:
        return int(100 * (level ** 1.5) + level * 20)
    
    @classmethod
    def get_progress(cls, player_id: int, skill_type: str) -> dict:
        skill = cls.get_or_create_skill(player_id, skill_type)
        required = cls._get_required_exp(skill.level)
        progress = (skill.exp / required) * 100 if required > 0 else 0
        
        return {
            'level': skill.level,
            'current_exp': skill.exp,
            'required_exp': required,
            'progress': progress
        }
    
    @classmethod
    def get_all_skills(cls, player_id: int) -> list:
        return cls.select().where(cls.player_id == player_id)


def init_skill_database():
    with db:
        db.create_tables([Skill], safe=True)
