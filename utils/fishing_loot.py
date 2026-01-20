import json
import random
from pathlib import Path


class FishingLootTable:
    """釣魚掉落表 - 動態載入魚種配置"""
    
    def __init__(self, json_path: str = "data/fishing_loot.json"):
        """
        初始化掉落表
        
        參數：
            json_path: JSON 配置檔案路徑
        """
        self.fish_list = []
        self.total_weight = 0
        self._load_from_json(json_path)
    
    def _load_from_json(self, json_path: str):
        """從 JSON 載入魚種配置"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.fish_list = data.get('fish', [])
            self.total_weight = sum(fish.get('weight', 1) for fish in self.fish_list)
            
            print(f"[FishingLootTable] 載入 {len(self.fish_list)} 種魚，總權重 {self.total_weight}")
        
        except FileNotFoundError:
            print(f"[FishingLootTable] 錯誤：找不到檔案 {json_path}")
            self.fish_list = []
            self.total_weight = 0
        except Exception as e:
            print(f"[FishingLootTable] 載入失敗：{e}")
            self.fish_list = []
            self.total_weight = 0
    
    def roll(self) -> dict:
        """
        抽取一條魚
        
        返回：dict，包含魚的完整資訊
            {
                'item_key': 'salmon',
                'name': '鮭魚',
                'experience': 7,  # 已隨機
                'value': 5,
                'weight': 30
            }
        
        如果沒有可用魚種，返回 None
        """
        if not self.fish_list or self.total_weight == 0:
            return None
        
        # 權重隨機抽取
        roll = random.uniform(0, self.total_weight)
        current = 0
        
        for fish in self.fish_list:
            current += fish.get('weight', 1)
            if roll <= current:
                # 隨機計算經驗值
                exp_min = fish.get('experience_min', 1)
                exp_max = fish.get('experience_max', 1)
                experience = random.randint(exp_min, exp_max)
                
                return {
                    'item_key': fish['item_key'],
                    'name': fish['name'],
                    'experience': experience,
                    'value': fish['base_value'],
                    'weight': fish.get('weight', 1)
                }
        
        # 理論上不會到這裡，但作為備用
        return self.fish_list[0] if self.fish_list else None
    
    def get_fish_info(self, item_key: str) -> dict:
        """
        取得特定魚種的資訊
        
        參數：
            item_key: 魚的鍵值（如 "salmon"）
        
        返回：魚的資訊字典，找不到則返回 None
        """
        for fish in self.fish_list:
            if fish['item_key'] == item_key:
                return fish
        return None
