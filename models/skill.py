from peewee import *
from enum import Enum

from models.player import Player
from models.generic import db


class SkillType(str, Enum):
    MINING = "mining"
    FISHING = "fishing"
    GARDENING = "gardening"


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
    def get_or_create_skill(cls, player_id: int, name: SkillType):
        skill, _ = cls.get_or_create(player_id = player_id, name = name)
        return skill
    
    @classmethod
    def add_experience(cls, player_id: int, name: SkillType, amount: int) -> dict:
        skill = cls.get_or_create_skill(player_id, name)
        
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
