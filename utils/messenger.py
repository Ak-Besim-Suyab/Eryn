"""
這個工具用於集中推送最後需要印出的 Embed, View 訊息
通常該工具只會存在於 Cogs 內，將 interaction 留在邏輯外圍，盡可能不傳入更深層的邏輯處理
"""
import discord

from models import message_manager
from cores.logger import logger
from ui.views import view_registry

from data.type import TitleType, ColorType
from data.event import Event
from data.payload import Payload

class Messenger:
    """
    印出訊息的主要入口
    """
    @classmethod
    async def send(cls, event: Event, interaction: discord.Interaction, ephemeral: bool = False):

    #sender: str # 訊息發送的主體，必須填入否則報錯，同時也用於判斷 player 與 non-player
        if not isinstance(event, Event):
            logger.error(f"event 類別錯誤, event: {event}")
            return

        embed, view = cls.create(event.payload, interaction)

        await interaction.response.send_message(embed = embed, view = view, ephemeral = ephemeral)

    @classmethod
    def create(cls, payload: Payload = None, interaction: discord.Interaction = None) -> discord.Embed:

        message_name = payload.message.title
        message = message_manager.get(message_name)

        if not message:
            logger.error(f"message 找不到格式內容, message id: {message_name}")
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
            view_object = view_registry.get(message.view)

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
            case ColorType.LIGHT_GREY:
                return discord.Color.light_grey()
            case ColorType.DARK_GREY:
                return discord.Color.dark_grey()
            case ColorType.DARK_THEME:
                return discord.Color.dark_theme()
    
    @classmethod
    def get_style(cls, style: str) -> discord.ButtonStyle:
        """這個方法會根據字串獲取對應 discord.ButtonStyle"""
        match style:
            case "primary":
                return discord.ButtonStyle.primary

_instance = Messenger()
send = _instance.send

