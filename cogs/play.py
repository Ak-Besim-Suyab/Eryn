import discord 
from discord.ext import commands
from discord import app_commands

from interface.menu import MenuEmbed, MenuView

from configuration import GUILD_TH_HAVEN, GUILD_AK_BESIM, ADMIN_BOOLEAN

class PlayCog(commands.Cog, name="玩"):
    def __init__(self, bot):
        self.bot = bot

    # @app_commands.default_permissions(administrator=ADMIN_BOOLEAN)
    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="玩", description="開始遊玩艾琳的遊戲")
    async def play(self, interaction: discord.Interaction):
        # 這裡之後會加上狀態判斷，如果玩家處在特定的進度中（比如正在對話或戰鬥中）輸入這個指令會直接復原進度
        # 沒有的話則會進入主選單
        
        embed, view = MenuEmbed(interaction), MenuView()

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(PlayCog(bot))