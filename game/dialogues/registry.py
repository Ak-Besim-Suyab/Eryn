from dataclasses import dataclass, field
from cores import Registry

@dataclass
class Component:
    style: str = "primary"
    label: str | None = None
    emoji: str | None = None
    callback: str | None = None

@dataclass
class Page:
    """
    `is_newtab`: 是否發送新的訊息 (send_message) 而非更新舊訊息 (edit_message)
    """
    title: str | None = None
    description: str | None = None
    color: str | None = None

    components: list[Component] = field(default_factory = list)

    is_newtab: bool = False

    def __post_init__(self):
        if self.components and isinstance(self.components[0], dict):
            self.components = [Component(**component) for component in self.components]

@dataclass
class Dialogue:
    pages: dict[int, Page] = field(default_factory = dict)

    def __post_init__(self):
        if self.pages and isinstance(next(iter(self.pages.values())), dict):
            self.pages = {int(number): Page(**page) for number, page in self.pages.items()}

    def get_page(self, page_number: int) -> Page | None:
        return self.pages.get(page_number)

class DialogueRegistry(Registry[Dialogue]):
    def __init__(self):
        super().__init__(model=Dialogue, path = "game/dialogues/assets")

# --------------------------------------
# 創建單例

dialogue_registry = DialogueRegistry()

"""
文本模塊

構思:
事件會抽取對應的文本 (dialogue) 

dialogue = dialogue_registry.get(dialog_name)

page = dialogue.get_page(page_number)

embed = discord.Embed()
embed.title = page.title
embed.description = page.description
embed.color = page.color

match page.author:
    case player:
        embed.set_author(name=player.display_name, icon_url=player.avatar.url)
    case _:
        pass
"""