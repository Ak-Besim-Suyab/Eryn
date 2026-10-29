from config import DICE_PATTERN

def parse(content: str) -> tuple[int, int] | None:

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