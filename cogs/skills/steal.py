import discord
import random
from discord.ext import commands
from discord import app_commands

from models.player import Player
from models.skill import Skill
from models.status import Status
from models.type import StatusType

from configuration import GUILD_TH_HAVEN, GUILD_AK_BESIM, ANNOUNCEMENT_CHANNEL

class Steal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.ctx_menu = app_commands.ContextMenu(name="偷竊", callback=self.context_steal)
        self.bot.tree.add_command(self.ctx_menu)

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="偷竊", description="偷取他人的物品")
    async def command_steal(self, interaction: discord.Interaction, member: discord.Member):
        await self.execute(interaction, member)

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    async def context_steal(self, interaction: discord.Interaction, member: discord.Member):
        await self.execute(interaction, member)

    async def execute(self, interaction: discord.Interaction, member: discord.Member):

        if random.random() < 0.35:
            await interaction.response.send_message("偷竊失敗！")
            return
        
        stole_currency = random.randint(1, 5)
        experience = random.randint(1, 5)

        Player.add_balance(interaction.user.id, stole_currency)
        Player.add_experience(interaction.user.id, experience)
        Status.add(interaction.user.id, StatusType.UNLUCKY, 1)

        await interaction.response.defer()

        if member.bot:
            await interaction.followup.send("喵喵喵！咪沒有東西可以偷！")
            return

        if interaction.user.id == member.id:
            await interaction.followup.send("你不能偷自己的物品！")
            return
            
        channel_id = ANNOUNCEMENT_CHANNEL.get(interaction.guild.id)

        # 這段可能有需要修正的邏輯，之後再調整
        if not channel_id:
            # 因為沒設定頻道就直接不傳送公告訊息，但如果是使用指令，發送到使用指令的頻道
            await interaction.followup.send("偷竊成功！")
            return

        channel = interaction.guild.get_channel(channel_id)

        description = [
            f"{interaction.user.display_name} 成功從 {member.display_name} 偷取物品！"
        ]
            
        field = [
            f"金幣 +{stole_currency}",
            f"經驗值 +{experience}",
        ]

        embed = discord.Embed()
        embed.color = discord.Color.gold()
        embed.description = "\n".join(description)

        embed.add_field(name="獲得物品：", value=field, inline=False)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

        if channel:
            await channel.send(embed=embed)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Steal(bot))