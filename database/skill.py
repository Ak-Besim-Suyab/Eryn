from peewee import *
from database.generic import db
from database.player import Player


class Skill(Model):
    # associated skills in Player.skills
    player = ForeignKeyField(Player, backref='skills', on_delete='CASCADE')

    name = TextField()
    level = IntegerField(default = 1)
    experience = IntegerField(default = 0)

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
    
    # this method can return a payload dict for level up info.
    @classmethod
    def add_experience(cls, player_id: int, skill_name: str, amount: int) -> dict:
        skill = cls.get_or_create_skill(player_id, skill_name)
        
        skill.experience += amount
        
        old_level = skill.level
        
        while skill.experience >= cls._get_required_exp(skill.level):
            skill.experience -= cls._get_required_exp(skill.level)
            skill.level += 1
        
        skill.save()

        level_payload = {
            'level': skill.level,
            'experience': skill.experience,
            'is_level_up': skill.level > old_level,
        }

        return level_payload
    
    @staticmethod
    def _get_required_exp(level: int) -> int:
        return int(100 * (level ** 1.5) + level * 20)
    
    @classmethod
    def get_progress(cls, player_id: int, skill_type: str) -> dict:
        skill = cls.get_or_create_skill(player_id, skill_type)
        required = cls._get_required_exp(skill.level)
        progress = (skill.experience / required) * 100 if required > 0 else 0
        
        return {
            'level': skill.level,
            'current_experience': skill.experience,
            'required_experience': required,
            'progress': progress
        }
    
    @classmethod
    def get_all_skills(cls, player_id: int) -> list:
        return cls.select().where(cls.player_id == player_id)


def init_skill_database():
    with db:
        db.create_tables([Skill], safe=True)
