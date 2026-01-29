import discord
from discord.ext import commands
from discord import app_commands

from context import GUILD_TH_HAVEN, GUILD_AK_BESIM

from session.role_session import RoleSession

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="身分組", description="檢視你可以存取的身分組")
    async def role(self, interaction: discord.Interaction):
        await RoleSession().start(interaction)

async def setup(bot):
    await bot.add_cog(Role(bot))