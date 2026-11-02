import discord
from discord import ui
from discord.ext import commands
from discord import app_commands

class GameSpinnerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="遊戲轉盤", description="幫助你挑選今天想玩的遊戲！")
    async def game_spinner(self, interaction: discord.Interaction):
        pass

class GameSpinnerView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        pass


class GameSelect(ui.Select):
    def __init__(self):
        super().__init__()
        pass

class NumberSelect(ui.Select):
    def __init__(self):
        super().__init__()
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(GameSpinnerCog(bot))