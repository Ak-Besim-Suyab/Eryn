import discord
from discord.ext import commands
from discord import app_commands

#from player_manager import player_manager

GUILD_TH_HAVEN = discord.Object(id=1193049715638538280)
GUILD_AK_BESIM = discord.Object(id=1190027756482859038)

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('[Command] inventory command Loaded')

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="inventory", description="查看你的背包")
    async def inventory(self, interaction: discord.Interaction):
        player_manager = self.bot.get_cog("PlayerManager")
        player = player_manager.get_player(interaction.user.id, interaction.user.display_name)
        
        embed = player.inventory.display(player)
        await interaction.response.send_message(embed=embed) # 發送 embed 訊息

async def setup(bot):
    await bot.add_cog(Inventory(bot))
