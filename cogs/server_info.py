import discord
from discord import app_commands
from discord.ext import commands
import json
import os

RULE_FILE = "data/server_rules.json"


def load_rules():
    if not os.path.exists(RULE_FILE):
        return {}
    with open(RULE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


class ServerInfo(commands.Cog):
    """伺服器規則 / 伺服器資訊模塊"""

    def __init__(self, bot):
        self.bot = bot

    # -------------------------------------------------
    # /server_rules
    # -------------------------------------------------
    @app_commands.command(name="server_rules", description="顯示伺服器規則")
    async def server_rules(self, interaction: discord.Interaction):

        rules = load_rules()

        if not rules:
            return await interaction.response.send_message("尚未設定伺服器規則。", ephemeral=True)

        embed = discord.Embed(
            title="📘 伺服器規則",
            color=discord.Color.blue()
        )

        for number, text in rules.items():
            embed.add_field(
                name=f"規則 {number}",
                value=text,
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    # -------------------------------------------------
    # /server_info
    # -------------------------------------------------
    @app_commands.command(name="server_info", description="顯示伺服器介紹/相關資訊")
    async def server_info(self, interaction: discord.Interaction):

        guild = interaction.guild
        if guild is None:
            return await interaction.response.send_message("只能在伺服器內使用。", ephemeral=True)

        embed = discord.Embed(
            title=f"{guild.name} 伺服器資訊",
            color=discord.Color.green()
        )

        embed.add_field(name="成員數", value=str(guild.member_count))
        embed.add_field(name="創立時間", value=guild.created_at.strftime("%Y-%m-%d"))
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
