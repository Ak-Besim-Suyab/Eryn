import discord
from discord.ext import commands
from discord import app_commands

from context import Context
from state.look_state import LookState

class Look(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('[Logs/Cogs] Command loaded: look')

    @app_commands.guilds(Context.GUILD_TH_HAVEN, Context.GUILD_AK_BESIM)
    @app_commands.command(name="look", description="查看你所處的地區四周有什麼")
    async def look(self, interaction: discord.Interaction):
        state = LookState(interaction)
        await state.start()

async def setup(bot):
    await bot.add_cog(Look(bot))