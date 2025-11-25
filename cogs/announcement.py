import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime

from context import Context

from ui.button import AboutBotButton

ANNOUNCEMENT_FILE = "data/announcements.json"


def load_announcements() -> dict:
    """讀取預先設定好的公告 JSON。"""
    if not os.path.exists(ANNOUNCEMENT_FILE):
        return {}
    with open(ANNOUNCEMENT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_color(raw_color) -> discord.Color:
    """從 JSON 的 color 轉成 discord.Color。
    支援：
    - 整數（例如 16776960）
    - 十六進位字串（例如 '#ffcc00' 或 'ffcc00'）
    其他情況則回傳預設顏色。
    """
    if isinstance(raw_color, int):
        try:
            return discord.Color(raw_color)
        except ValueError:
            return discord.Color.default()

    if isinstance(raw_color, str):
        try:
            value = int(raw_color.lstrip("#"), 16)
            return discord.Color(value)
        except ValueError:
            return discord.Color.default()

    return discord.Color.default()


def build_embed_from_data(data: dict) -> discord.Embed:
    """根據 JSON 設定組出一個 Embed。"""

    title = data.get("title")
    # description 可用 description 或 content 當別名
    description = data.get("description") or data.get("content")

    raw_color = data.get("color")
    color = parse_color(raw_color) if raw_color is not None else discord.Color.default()

    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    # 是否附上目前時間
    if data.get("use_timestamp"):
        embed.timestamp = datetime.utcnow()

    # thumbnail
    thumbnail_url = data.get("thumbnail_url")
    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    # image
    image_url = data.get("image_url")
    if image_url:
        embed.set_image(url=image_url)

    # footer
    footer_text = data.get("footer_text")
    footer_icon_url = data.get("footer_icon_url")
    if footer_text or footer_icon_url:
        embed.set_footer(
            text=footer_text or discord.Embed.Empty,
            icon_url=footer_icon_url or discord.Embed.Empty
        )

    # fields
    fields = data.get("fields", [])
    if isinstance(fields, list):
        for field in fields:
            name = field.get("name")
            value = field.get("value")
            if not name or not value:
                continue
            inline = field.get("inline", False)
            embed.add_field(name=name, value=value, inline=inline)

    return embed


class Announcement(commands.Cog):
    """單純從 JSON 發送預先寫好的公告。"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guilds(Context.GUILD_TH_HAVEN, Context.GUILD_AK_BESIM)
    @app_commands.command(
        name="announce_send",
        description="從 JSON 發送預先設定的公告到指定頻道（僅管理員）"
    )
    @app_commands.describe(
        announcement_id="announcements.json 裡的公告鍵名",
        channel="要發送的頻道"
    )
    async def announce_send(
        self,
        interaction: discord.Interaction,
        announcement_id: str,
        channel: discord.TextChannel
    ):
        # 管理員權限檢查
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "你沒有權限發送公告。",
                ephemeral=True
            )

        announcements = load_announcements()

        if not announcements:
            return await interaction.response.send_message(
                "目前沒有可用的公告設定（announcements.json 為空或不存在）。",
                ephemeral=True
            )

        if announcement_id not in announcements:
            return await interaction.response.send_message(
                f"找不到公告 ID：`{announcement_id}`。",
                ephemeral=True
            )

        # 這一筆公告的設定
        config = announcements[announcement_id]

        # 可選的純文字內容（會在 Embed 前一起發）
        plain_content = config.get("content") or config.get("plain_text")

        # embed 設定：
        # - 如果有 config["embed"]，就用 embed 下面那層
        # - 否則直接把這層當 embed 設定（方便簡化寫法）
        embed_data = config.get("embed", config)
        embed = build_embed_from_data(embed_data)

        view = discord.ui.View(timeout=None)
        view.add_item(AboutBotButton())

        await channel.send(content=plain_content, embed=embed, view=view)

        await interaction.response.send_message(
            f"已將公告 **`{announcement_id}`** 發送到 {channel.mention}",
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Announcement(bot))
