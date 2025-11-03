import discord
from discord.ext import commands
from discord import app_commands

from context import Context

class Look(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('[Logs/Cogs] Command loaded: look')

    @app_commands.guilds(Context.GUILD_TH_HAVEN, Context.GUILD_AK_BESIM)
    @app_commands.command(name="look", description="查看你所處的地區四周有什麼")
    async def look(self, interaction: discord.Interaction):
        state_machine = Context.state_machine
        look_state = state_machine.create("look", interaction)
        await look_state.start()

async def setup(bot):
    await bot.add_cog(Look(bot))