"""
這個模塊
"""
from dataclasses import dataclass, field

from data.type import TitleType, ColorType

from cores.manager import Manager
from cores.logger import logger

@dataclass
class Thumbnail:
    type: TitleType | str = TitleType.DEFAULT
    url: str = ""

@dataclass
class Field:
    name: str
    value: str
    inline: bool = False

@dataclass
class Message:
    """
    thumbnail 預設為空, 此舉是避免訊息在創建時總是填入模板圖像
    """
    id: str
    title: str = ""
    title_type: TitleType | str = TitleType.DEFAULT
    color: ColorType | str = ColorType.GOLD
    description: str = ""
    image: str = ""
    footer: str = ""

    fields: list[Field] = field(default_factory = list)
    thumbnail: Thumbnail | dict = None

    view: str = None

    has_author: bool = False

    def __post_init__(self):
        # 這裡是後處理，將串列與字典展開並轉換成物件，再打包回變數內
        if self.fields and isinstance(self.fields, list) and isinstance(self.fields[0], dict):
            self.fields = [Field(**field) for field in self.fields]
        
        # 檢查字串格式是否存在規定的 TitleType 格式內，否則給予預設值
        if isinstance(self.title_type, str):
            try:
                self.title_type = TitleType(self.title_type)
            except ValueError:
                logger.error(f"出現不支援的 title_type: {self.title_type}, 出現的 id: {self.id}")
                self.title_type = TitleType.DEFAULT
        
        # 檢查字串格式是否存在規定的 ColorType 格式內，否則給予預設值
        if isinstance(self.color, str):
            try:
                self.color = ColorType(self.color)
            except ValueError:
                logger.error(f"出現不支援的 color: {self.color}, 出現的 id: {self.id}")
                self.color = ColorType.GOLD
        
        if isinstance(self.thumbnail, dict):
            self.thumbnail = Thumbnail(**self.thumbnail)
            if isinstance(self.thumbnail.type, str):
                try:
                    self.thumbnail.type = TitleType(self.thumbnail.type)
                except ValueError:
                    logger.error(f"出現不支援的 thumbnail.type: {self.thumbnail.type}, 出現的 id: {self.id}")
                    self.thumbnail.type = TitleType.DEFAULT

class MessageManager(Manager[Message]):
    def __init__(self):
        super().__init__(
            model = Message,
            path = "assets/messages"
        )

# 創建唯一實例
message_manager = MessageManager()