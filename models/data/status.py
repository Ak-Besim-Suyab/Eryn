from dataclasses import dataclass, field
from cores.manager import Manager

@dataclass
class Stack:
    min: int = 1
    max: int = 1

@dataclass
class Status:
    id: str
    name: str
    description: str
    stack: Stack | dict = field(default_factory = lambda: Stack(min = 1, max = 1))

    def __post_init__(self):
        # 這裡是後處理，把宣告後的物件裡的層數 (stack) 與等級 (level) 轉換成 Range 物件，然後再放回去
        if isinstance(self.stack, dict):
            self.stack = Stack(**self.stack)

class StatusManager(Manager[Status]):
    def __init__(self):
        super().__init__(
            model = Status, 
            path = "assets/statuses"
        )

status_manager = StatusManager()