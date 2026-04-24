from peewee import *

from systems.models.player import Player
from data.type import ActionType
from config import db

class Skill(Model):
    player = ForeignKeyField(Player, backref='skills', on_delete='CASCADE')
    name = CharField()
    level = IntegerField(default = 1)
    experience = IntegerField(default = 0)

    class Meta:
        database = db
        indexes = (
            (('player', 'name'), True),
        )
    
    @classmethod
    def add_experience(cls, player_id: int, name: ActionType, amount: int) -> dict:
        skill, _ = cls.get_or_create(player_id = player_id, name = name)
        
        skill.experience += amount
        
        while skill.experience >= cls._get_required_exp(skill.level):
            skill.experience -= cls._get_required_exp(skill.level)
            skill.level += 1
        
        skill.save()
    
    @staticmethod
    def _get_required_exp(level: int) -> int:
        return int(100 * (level ** 1.5) + level * 20)


def init_skill_database():
    with db:
        db.create_tables([Skill], safe=True)
