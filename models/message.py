import discord
from dataclasses import dataclass, field
from cores.manager import Manager

from cores.logger import logger

@dataclass
class Field:
    name: str
    value: str
    inline: bool = False

@dataclass
class Message:
    id: str

    title: str = ""
    description: str = ""
    color: str = ""
    image: str = ""

    fields: list[Field] = field(default_factory = list)

    has_author: bool = False

    def __post_init__(self):
        # 這裡是後處理
        if self.fields and isinstance(self.fields, list) and isinstance(self.fields[0], dict):
            self.fields = [Field(**field) for field in self.fields]

class MessageManager(Manager[Message]):
    def __init__(self):
        super().__init__(
            model = Message,
            path = "assets/messages"
        )

    def create(self, message_id: str, payload: dict = None, user: discord.User | discord.Member = None) -> discord.Embed:

        message = self.get(message_id)
        if not message:
            logger.error(f"message 找不到格式內容, message id: {message_id}")
            return

        if not payload:
            payload = {}

        embed = discord.Embed()

        if message.title:
            embed.title = message.title.format(**payload)

        if message.description:
            embed.description = message.description.format(**payload)
        
        if message.color:
            embed.color = self.get_color(message.color)
        else:
            embed.color = self.get_color("gold")

        if message.fields:
            for field in message.fields:
                embed.add_field(
                    name = field.name.format(**payload), 
                    value = field.value.format(**payload), 
                    inline=field.inline
                )
        
        if message.image:
            embed.set_image(url=message.image)

        if message.has_author and user:
            embed.set_author(
                name = user.display_name, 
                icon_url = user.display_avatar.url
            )
        elif message.has_author and not user:
            logger.debug(f"message 需要印出使用者資料, 但沒有找到使用者, message id: {message.id}")

        return embed

    def get_color(self, color: str) -> discord.Color:
        """
        這個方法會根據字串獲取對應 discord.Color, 目前內建方法應該足夠使用, 若有需要另外再擴充
        """
        match color:
            case "gold":
                return discord.Color.gold()
            case "dark_gold":
                return discord.Color.dark_gold()

# 創建唯一實例
message_manager = MessageManager()