from peewee import *
from database.generic import db
from database.player import Player


class Skill(Model):
    """玩家技能等級系統 - 用於 fishing, mining 等技能"""
    player = ForeignKeyField(Player, backref='skills', on_delete='CASCADE')
    skill_type = TextField()  # 'fishing', 'mining', 'cooking' 等
    level = IntegerField(default=1)
    experience = IntegerField(default=0)

    class Meta:
        database = db
        indexes = (
            (('player', 'skill_type'), True),  # 複合主鍵：防止同一玩家有重複的技能
        )
    
    @classmethod
    def get_or_create_skill(cls, player_id: int, skill_type: str):
        """
        取得或創建玩家技能等級記錄
        
        參數：
            player_id: 玩家 ID
            skill_type: 技能類型（'fishing', 'mining' 等）
        """
        skill, created = cls.get_or_create(
            player_id=player_id,
            skill_type=skill_type
        )
        return skill
    
    @classmethod
    def add_experience(cls, player_id: int, amount: int, skill_type: str) -> dict:
        """
        增加技能經驗值，自動處理升級
        
        參數：
            player_id: 玩家 ID
            amount: 增加的經驗值
            skill_type: 技能類型（'fishing', 'mining' 等）
        
        返回：dict，包含：
            {
                'level': 當前等級,
                'experience': 當前經驗值,
                'leveled_up': 是否升級,
                'new_levels': 升級到的新等級列表
            }
        """
        skill = cls.get_or_create_skill(player_id, skill_type)
        
        skill.experience += amount
        
        old_level = skill.level
        new_levels = []
        
        # 使用 while 循環處理連續升級的情況
        while skill.experience >= cls._get_required_exp(skill.level):
            # 扣除本級所需的經驗
            skill.experience -= cls._get_required_exp(skill.level)
            # 升級
            skill.level += 1
            new_levels.append(skill.level)
        
        # 保存到數據庫
        skill.save()
        
        # 返回結果字典
        return {
            'level': skill.level,
            'experience': skill.experience,
            'leveled_up': skill.level > old_level,
            'new_levels': new_levels
        }
    
    @staticmethod
    def _get_required_exp(level: int) -> int:
        """
        計算升級所需的經驗值
        
        公式：required_exp(n) = 100 * (n ^ 1.5) + 20 * n
        （與 Character 系統相同的升級公式）
        """
        return int(100 * (level ** 1.5) + level * 20)
    
    @classmethod
    def get_progress(cls, player_id: int, skill_type: str) -> dict:
        """
        取得玩家技能的進度信息（用於顯示進度條）
        
        參數：
            player_id: 玩家 ID
            skill_type: 技能類型
        
        返回：dict，包含：
            {
                'level': 當前等級,
                'current_exp': 當前經驗值,
                'required_exp': 升到下一級需要的經驗值,
                'progress': 進度百分比 (0-100)
            }
        """
        skill = cls.get_or_create_skill(player_id, skill_type)
        required = cls._get_required_exp(skill.level)
        progress = (skill.experience / required) * 100 if required > 0 else 0
        
        return {
            'level': skill.level,
            'current_exp': skill.experience,
            'required_exp': required,
            'progress': progress
        }
    
    @classmethod
    def get_all_skills(cls, player_id: int) -> list:
        """
        取得玩家的所有技能
        
        返回：Skill 對象列表
        """
        return cls.select().where(cls.player_id == player_id)


def init_skill_database():
    with db:
        db.create_tables([Skill])
