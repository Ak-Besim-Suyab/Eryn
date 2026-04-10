"""
這個類別用於推送最後需要印出 Embed 訊息的方法
被賦予裝飾器的方法若訊息類別有對應的參數, 則需要回傳 payload, 將參數傳回訊息結構
這裡不參與任何邏輯處理

範例: 
from utils import embed

@embed.emit("daily")
async def daily(interaction: discord.Interaction):
    ...
    return payload
"""
import discord
from functools import wraps
from models import message_manager
from models.type import TitleType, ColorType
from cores.logger import logger


class Embed:

    @classmethod
    def emit(cls, message_id: str):
        def decorator(func):
            @wraps(func)
            async def wrapper(command, interaction: discord.Interaction, *args, **kwargs):

                payload = await func(command, interaction, *args, **kwargs)
                if not payload:
                    return

                embed = cls.create(message_id, payload, interaction)
                await interaction.response.send_message(embed=embed)
                
                return payload
            
            return wrapper
        
        return decorator
    
    @classmethod
    def create(cls, message_id: str, payload: dict = None, interaction: discord.Interaction = None) -> discord.Embed:

        message = message_manager.get(message_id)
        if not message:
            logger.error(f"message 找不到格式內容, message id: {message_id}")
            return

        if not payload:
            payload = {}

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

        return embed

    @classmethod
    def get_color(cls, color: str) -> discord.Color:
        """這個方法會根據字串獲取對應 discord.Color"""
        match color:
            case ColorType.GOLD:
                return discord.Color.gold()
            case ColorType.DARK_GOLD:
                return discord.Color.dark_gold()