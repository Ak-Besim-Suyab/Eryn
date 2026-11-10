from dataclasses import dataclass, field
from lib.util import SafeDict
import random

@dataclass
class Line:
    """
    隨機文本資料物件, 用於生成隨機文本, 宣告後請使用 random() 函式來取得結果, 可以加入字典參數替換佔位符
    """
    lines: list[str] = field(default_factory=list)

    def random(self, **kwargs) -> str:
        return random.choice(self.lines).format_map(SafeDict(**kwargs))