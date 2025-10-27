import discord
from discord.ext import commands
from discord import app_commands

import asyncio

from player_manager import player_manager

GUILD_TH_HAVEN = discord.Object(id=1193049715638538280)
GUILD_AK_BESIM = discord.Object(id=1190027756482859038)

class Perform(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.previous_time = {}
        self.cooldown_time = 10

        print('[Command] Perform command initialized successfully.')

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="perform", description="在這裡進行演奏")
    async def mining(self, interaction: discord.Interaction):
        player = player_manager.get_player(interaction.user.id, interaction.user.display_name)
        #now = asyncio.get_event_loop().time()

        #print(self.previous_time)

        # if player in self.previous_time:
        #     if now >= self.previous_time[player]:
        #         print("your time has come!")
        #         del self.previous_time[player]
        #     else:
        #         print("your time not come yet.")
        # else:
        #     print("no timer, create one.")
        #     self.previous_time[player] = now + self.cooldown_time
        #     print(self.previous_time)

        #await interaction.response.send_message(f"演奏測試！")
        #await asyncio.sleep(3)
        #await interaction.edit_original_response(content=f"演奏完畢！")

class PerformView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="再次演奏", style=discord.ButtonStyle.primary)
    async def remine(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"演奏測試！")
        await asyncio.sleep(3)
        await interaction.response.edit_message(f"測試完畢！", view=self)

async def setup(bot):
    await bot.add_cog(Perform(bot))