import discord
from discord.ext import commands
from discord import app_commands
import random

from context import Context

GUILD_TH_HAVEN = discord.Object(id=1193049715638538280)
GUILD_AK_BESIM = discord.Object(id=1190027756482859038)

class World(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('[Logs/Cogs] Command /world loaded.')

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="world", description="查看地圖，前往")
    async def world(self, interaction: discord.Interaction):
        embed = discord.Embed(
                    title=f"{interaction.user.display_name}",
                    description=f"你目前的位置：\n想去哪？",
                    color=discord.Color.greyple()
                )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1193049715638538283/1429993112633085963/Bakery_pixel_art3.png")
        await interaction.response.send_message(embed=embed, view=WorldView())

class WorldView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(WorldSelect())

class WorldSelect(discord.ui.Select):
    def __init__(self):
        self.worlds = Context.get_world_entry()
        options = []

        for world_id, world_name in self.worlds.items():
            options.append(discord.SelectOption(label=world_name, value=world_id, emoji="🗺️"))

        super().__init__(
            placeholder="選擇地圖",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        player_manager = Context.get_manager("player_manager")
        player = player_manager.get_player(interaction)
        choice = self.values[0]

        embed = discord.Embed(
                    title=f"{interaction.user.display_name}",
                    description=f"你成功到達了：{self.worlds.get(choice)}",
                    color=discord.Color.greyple()
                )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1193049715638538283/1429993112633085963/Bakery_pixel_art3.png")

        player.location = choice

        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(World(bot))