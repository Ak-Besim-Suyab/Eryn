import random
import bisect
from config import DICE_PATTERN

from dataclasses import dataclass

from data.enums import Outcome

@dataclass
class RollResult:
    roll       : int     # 擲骰結果
    modifier   : int     # 修正值
    difficulty : int     # 難度
    outcome    : Outcome # 檢定結果

    @property
    def total(self) -> int:
        """擲骰總和（擲骰結果 + 修正值）"""
        return self.roll + self.modifier

    def is_success(self) -> bool:
        """是否成功"""
        return self.outcome in (Outcome.SUCCESS, Outcome.CRITICAL_SUCCESS)

def parse(content: str) -> tuple[int, int] | None:
    """
    解析多面骰並返回數量與面數, 多面骰必須為桌上型遊戲格式, 例如: `1D20`
    """
    dice = DICE_PATTERN.match(content)

    if not dice:
        return None

    # 取得匹配數量與面數
    count = int(dice.group(1) or 1)
    sides = int(dice.group(2))

    # 檢查數量與面數是否合法, 數量不能小於1 (e.g. 0D10為無效擲骰), 面數不能小於2 (e.g. 1D1為無效擲骰)
    if count < 1 or sides < 2:
        return None

    return count, sides

def roll(sides: int, difficulty: int = 5, modifier: int = 0) -> RollResult:
    """
    計算指定面數的擲骰結果
    """
    roll = random.randint(1, sides)

    index = bisect.bisect([2, difficulty, sides], roll)
    outcome = Outcome(index)
    
    return RollResult(roll, modifier, difficulty, outcome)