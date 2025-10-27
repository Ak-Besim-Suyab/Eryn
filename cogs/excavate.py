import discord
from discord.ext import commands
from discord import app_commands

from context import Context
from state.excavate_state import ExcavateState

class Excavate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('[Logs/Cogs] Command loaded: excavate')

    @app_commands.guilds(Context.GUILD_TH_HAVEN, Context.GUILD_AK_BESIM)
    @app_commands.command(name="excavate", description="在你所處的地區嘗試挖掘")
    async def excavate(self, interaction: discord.Interaction):
        state = ExcavateState(interaction)
        await state.start()

async def setup(bot):
    await bot.add_cog(Excavate(bot))