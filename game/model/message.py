from dataclasses import dataclass, field

from .embed import Embed
from .view import View

@dataclass
class Page:
    """
    該類別負責讀取並組裝所有訊息元件

    `ephemeral`: 是否為私密訊息
    `is_newtab`: 是否發送新訊息 (send_message) 而非更新舊訊息 (edit_message)
    `auto`: 是否自動翻頁, 啟用時會在該則訊息發送後繼續發送下則訊息, 遇到非自動翻頁的訊息時預期應停止
    `auto_delay`: 自動翻頁的間隔時間, 該變數用於控制 asyncio.sleep 的時間長度
    """
    ephemeral: bool = False
    newtab: bool = True
    auto: bool = False
    auto_delay: float = 3.0

    embeds: list[Embed] = field(default_factory = list)
    view: View = None

    def __post_init__(self):
        if self.embeds and isinstance(self.embeds, list) and isinstance(self.embeds[0], dict):
            self.embeds = [Embed(**e) for e in self.embeds]

        if self.view and isinstance(self.view, dict):
            self.view = View(**self.view)

@dataclass
class Message:
    """
    外部資料設計時，傳入的資料屬於串列，但在這裡會轉換成字典，以便找查與讀取
    """
    pages: list[Page] | dict[int, Page] = field(default_factory = list)

    def __post_init__(self):
        if self.pages and isinstance(self.pages, list) and isinstance(self.pages[0], dict):
            self.pages = {int(k): Page(**v) for k, v in enumerate(self.pages, start=1)}

    def get_page(self, number: int) -> Page | None:
        return self.pages.get(number)