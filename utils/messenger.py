"""
這個裝飾器用於推送最後需要印出 Embed 訊息的方法
被賦予裝飾器的方法若訊息類別有對應的參數, 則需要回傳 payload, 將參數傳回訊息結構
這裡不參與任何邏輯處理
"""
import discord

from models import message_manager
from data.type import TitleType, ColorType
from cores.logger import logger
from utils.managers import view_manager
from data.event import Event
from data.payload import Payload

class Messenger:
    @classmethod
    async def send(cls, event: Event, interaction: discord.Interaction, ephemeral: bool = False):

        if not isinstance(event, Event):
            logger.error(f"event 類別錯誤, event: {event}")
            return

        embed, view = cls.create(event.payload.message.title, event.payload, interaction)

        await interaction.response.send_message(
            embed = embed,
            view = view,
            ephemeral = ephemeral
        )

    # @classmethod
    # def send(cls, message_id: str, ephemeral: bool = False):
    #     def decorator(func):
    #         @wraps(func)
    #         async def wrapper(command, interaction: discord.Interaction, *args, **kwargs):

    #             payload = await func(command, interaction, *args, **kwargs)
    #             if payload is False:
    #                 return
    #             if payload is None:
    #                 payload = {}

    #             embed, view = cls.create(message_id, payload, interaction)

    #             await interaction.response.send_message(
    #                 embed = embed,
    #                 view = view,
    #                 ephemeral = ephemeral
    #             )
                
    #             return payload
            
    #         return wrapper
        
    #     return decorator
    
    @classmethod
    def create(cls, message_id: str, payload: Payload = None, interaction: discord.Interaction = None) -> discord.Embed:

        message = message_manager.get(message_id)
        if not message:
            logger.error(f"message 找不到格式內容, message id: {message_id}")
            return

        if payload is None:
            payload = {}
        else:
            payload = payload.to_dict()

        embed = discord.Embed()

        # 防止同時產生 title 和 author, 加上對 has_author 的判斷.
        if not message.has_author:
            match message.title_type:
                case TitleType.DEFAULT:
                    embed.title = message.title.format(**payload)
                case TitleType.PLAYER:
                    if interaction:
                        embed.title = interaction.user.display_name
                case TitleType.BOT:
                    if interaction:
                        embed.title = interaction.client.user.display_name

        if message.description:
            embed.description = message.description.format(**payload)
        
        if message.color:
            embed.color = cls.get_color(message.color)
        else:
            embed.color = cls.get_color(ColorType.GOLD)

        if message.fields:
            for field in message.fields:
                embed.add_field(
                    name = field.name.format(**payload), 
                    value = field.value.format(**payload), 
                    inline=field.inline
                )
        
        if message.image:
            embed.set_image(url=message.image)

        if message.thumbnail:
            match message.thumbnail.type:
                case TitleType.DEFAULT:
                    embed.set_thumbnail(url=message.thumbnail.url)
                case TitleType.PLAYER:
                    if interaction:
                        embed.set_thumbnail(url=interaction.user.display_avatar.url)
                case TitleType.BOT:
                    if interaction:
                        embed.set_thumbnail(url=interaction.client.user.avatar.url)

        if message.has_author and interaction:
            embed.set_author(
                name = interaction.user.display_name, 
                icon_url = interaction.user.display_avatar.url
            )
        elif message.has_author and not interaction:
            logger.debug(f"message 需要印出使用者資料, 但沒有找到使用者, message id: {message.id}")

        if message.footer:
            embed.set_footer(text=message.footer.format(**payload))

        # view --
        view = discord.utils.MISSING
        if message.view:
            view_object = view_manager.get(message.view)

            if view_object:
                view = view_object()

        return embed, view

    @classmethod
    def get_color(cls, color: str) -> discord.Color:
        """這個方法會根據字串獲取對應 discord.Color"""
        match color:
            case ColorType.GOLD:
                return discord.Color.gold()
            case ColorType.DARK_GOLD:
                return discord.Color.dark_gold()
    
    @classmethod
    def get_style(cls, style: str) -> discord.ButtonStyle:
        """這個方法會根據字串獲取對應 discord.ButtonStyle"""
        match style:
            case "primary":
                return discord.ButtonStyle.primary

_instance = Messenger()
send = _instance.send