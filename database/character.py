from peewee import *
from database.generic import db
from database.player import Player


class Character(Model):
    player = ForeignKeyField(Player, backref='character', on_delete='CASCADE')
    level = IntegerField(default=1)
    experience = IntegerField(default=0)

    class Meta:
        database = db
    
    @classmethod
    def get_or_create_character(cls, player_id: int):
        character, created = cls.get_or_create(player_id=player_id)
        return character
    
    @classmethod
    def add_experience(cls, player_id: int, amount: int) -> dict:
        """
        增加經驗值，自動處理升級
        
        參數：
            player_id: 玩家 ID
            amount: 增加的經驗值
        
        返回：dict，包含：
            {
                'level': 當前等級,
                'experience': 當前經驗值,
                'leveled_up': 是否升級,
                'new_levels': 升級到的新等級列表
            }
        """
        character = cls.get_or_create_character(player_id)
        
        character.experience += amount
        
        old_level = character.level
        new_levels = []
        
        # 使用 while 循環處理連續升級的情況
        # 例如：一次性獲得大量經驗，可能同時升2-3級
        while character.experience >= cls._get_required_exp(character.level):
            # 扣除本級所需的經驗
            character.experience -= cls._get_required_exp(character.level)
            # 升級
            character.level += 1
            new_levels.append(character.level)
        
        # 保存到數據庫
        character.save()
        
        # 返回結果字典
        return {
            'level': character.level,
            'experience': character.experience,
            'leveled_up': character.level > old_level,
            'new_levels': new_levels  # 例如 [11, 12] 表示升級到了 11 和 12
        }
    
    @staticmethod
    def _get_required_exp(level: int) -> int:
        """
        計算升級所需的經驗值
        
        公式：required_exp(n) = 100 * (n ^ 1.5) + 20 * n
        
        解釋：
            - 基礎經驗：100
            - 等級指數：1.5（即 n 的 1.5 次方）
            - 線性加成：20 * n
            - 這樣設計使得越高的等級需要的經驗越多（指數增長）
        
        示例：
            level 1 -> 2：int(100 * 1^1.5 + 20*1) = 120 經驗
            level 10 -> 11：int(100 * 10^1.5 + 20*10) = 3375 經驗
            level 20 -> 21：int(100 * 20^1.5 + 20*20) = 8941 經驗
        """
        return int(100 * (level ** 1.5) + level * 20)
    
    @classmethod
    def get_progress(cls, player_id: int) -> dict:
        """
        取得玩家角色等級的進度信息（用於顯示進度條）
        
        參數：
            player_id: 玩家 ID
        
        返回：dict，包含：
            {
                'level': 當前等級,
                'current_exp': 當前經驗值,
                'required_exp': 升到下一級需要的經驗值,
                'progress': 進度百分比 (0-100)
            }
        
        示例：
            progress = Character.get_progress(123)
            print(f"等級：{progress['level']}")
            print(f"進度：{progress['progress']:.1f}%")
        """
        character = cls.get_or_create_character(player_id)
        required = cls._get_required_exp(character.level)
        progress = (character.experience / required) * 100 if required > 0 else 0
        
        return {
            'level': character.level,
            'current_exp': character.experience,
            'required_exp': required,
            'progress': progress
        }
    
    @classmethod
    def set_level(cls, player_id: int, level: int) -> dict:
        """
        直接設置玩家的等級（重設經驗值為 0）
        
        參數：
            player_id: 玩家 ID
            level: 要設置的等級（必須 >= 1）
        
        返回：dict，包含：
            {
                'level': 設置後的等級,
                'experience': 當前經驗值（0）,
                'old_level': 之前的等級
            }
        """
        if level < 1:
            raise ValueError("等級必須 >= 1")
        
        character = cls.get_or_create_character(player_id)
        old_level = character.level
        character.level = level
        character.experience = 0
        character.save()
        
        return {
            'level': character.level,
            'experience': character.experience,
            'old_level': old_level
        }
    
    @classmethod
    def set_experience(cls, player_id: int, experience: int) -> dict:
        """
        直接設置玩家的經驗值（不自動升級）
        
        參數：
            player_id: 玩家 ID
            experience: 要設置的經驗值（必須 >= 0）
        
        返回：dict，包含：
            {
                'level': 當前等級,
                'experience': 設置後的經驗值,
                'old_experience': 之前的經驗值
            }
        """
        if experience < 0:
            raise ValueError("經驗值必須 >= 0")
        
        character = cls.get_or_create_character(player_id)
        old_experience = character.experience
        character.experience = experience
        character.save()
        
        return {
            'level': character.level,
            'experience': character.experience,
            'old_experience': old_experience
        }


def init_character_database():
    with db:
        db.create_tables([Character])
