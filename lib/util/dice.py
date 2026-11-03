import random
import bisect
from config import DICE_PATTERN

from enum import IntEnum

BREAKPOINTS = [1, 5, 20]

# 檢定結果
class Outcome(IntEnum):
    CRITICAL_FAILURE = 0
    FAILURE = 1
    SUCCESS = 2
    CRITICAL_SUCCESS = 3

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

def roll(count: int, sides: int) -> list[int]:
    """
    計算指定數量與面數的擲骰結果，不論多少結果都返回為串列
    """
    return [random.randint(1, sides) for _ in range(count)]

def judge(roll: int):
    """
    使用 bisect 模組進行擲骰檢定，返回擲骰對應的檢定結果 `Outcomes` 用於判定成功與失敗
    .. Outcomes::
        `0` 為大失敗 (Critical Failure),
        `1` 為失敗 (Failure),
        `2` 為成功 (Success),
        `3` 為大成功 (Critical Success)
    """
    index = bisect.bisect(BREAKPOINTS, roll)
    return Outcome(index)