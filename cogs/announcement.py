import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime

ANNOUNCEMENT_FILE = "data/announcements.json"


def load_announcements():
    if not os.path.exists(ANNOUNCEMENT_FILE):
        return {}
    with open(ANNOUNCEMENT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_announcements(data):
    with open(ANNOUNCEMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class Announcement(commands.Cog):
    """簡易公告系統：新增公告、管理公告、發送公告"""

    def __init__(self, bot):
        self.bot = bot

    # -------------------------------------------------
    # /announce create
    # -------------------------------------------------
    @app_commands.command(name="announce_create", description="建立一則公告（僅管理員）")
    @app_commands.describe(title="公告標題", content="公告內容")
    async def announce_create(self, interaction: discord.Interaction, title: str, content: str):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("你沒有權限編輯公告。", ephemeral=True)

        announcements = load_announcements()

        new_id = str(len(announcements) + 1)
        announcements[new_id] = {
            "title": title,
            "content": content,
            "created_by": interaction.user.id,
            "timestamp": datetime.utcnow().isoformat()
        }

        save_announcements(announcements)

        await interaction.response.send_message(
            f"已新增公告 **#{new_id}**：{title}",
            ephemeral=True
        )

    # -------------------------------------------------
    # /announce_list
    # -------------------------------------------------
    @app_commands.command(name="announce_list", description="列出所有公告")
    async def announce_list(self, interaction: discord.Interaction):

        announcements = load_announcements()

        if not announcements:
            return await interaction.response.send_message("目前沒有公告。", ephemeral=False)

        embed = discord.Embed(
            title="📢 所有公告",
            color=discord.Color.gold()
        )

        for aid, data in announcements.items():
            embed.add_field(
                name=f"#{aid}｜{data['title']}",
                value=(data["content"][:100] + "...") if len(data["content"]) > 100 else data["content"],
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    # -------------------------------------------------
    # /announce_send id:1 channel:#general
    # -------------------------------------------------
    @app_commands.command(name="announce_send", description="將公告發送到指定頻道（管理員）")
    @app_commands.describe(announcement_id="公告 ID", channel="要發送的頻道")
    async def announce_send(self, interaction: discord.Interaction, announcement_id: str, channel: discord.TextChannel):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("你沒有權限發送公告。", ephemeral=True)

        announcements = load_announcements()

        if announcement_id not in announcements:
            return await interaction.response.send_message("找不到該公告 ID。", ephemeral=True)

        data = announcements[announcement_id]

        embed = discord.Embed(
            title=f"📢 {data['title']}",
            description=data["content"],
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"公告 ID: {announcement_id}")

        await channel.send(embed=embed)

        await interaction.response.send_message(
            f"已將公告 **#{announcement_id}** 發送到 {channel.mention}",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Announcement(bot))