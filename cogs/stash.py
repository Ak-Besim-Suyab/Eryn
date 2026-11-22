import discord
from discord.ext import commands
from discord import app_commands

import ui
from lib import information, view

class StashCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    stash_group = app_commands.Group(name="倉庫", description="查看倉庫")


    @stash_group.command(name="物品", description="查看物品")
    async def inventory_tab(self, interaction: discord.Interaction):
        await self.on_inventory_tab(interaction)

    @stash_group.command(name="資源", description="查看資源")
    async def resource_tab(self, interaction: discord.Interaction):
        await self.on_resource_tab(interaction)


    # 倉庫按鈕的元件事件監聽
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):

        # 檢查互動類型是否為元件，並確認有資料存在
        if interaction.type != discord.InteractionType.component or interaction.data is None:
            return

        # 檢查元件類型是否為 button
        if interaction.data.get("component_type") != 2:  
            return

        match interaction.data.get("custom_id"):
            case "inventory_tab":
                await self.on_inventory_tab(interaction, ephemeral=True); print("inventory tab opened by listener.")
            case "resource_tab":
                await self.on_resource_tab(interaction, ephemeral=True); print("resource tab opened by listener.")


    async def on_inventory_tab(self, interaction: discord.Interaction, ephemeral: bool = False):
        inventory = ui.Inventory(interaction.user)
        await interaction.response.send_message(view=inventory, ephemeral=ephemeral)

    async def on_resource_tab(self, interaction: discord.Interaction, ephemeral: bool = False):
        v = view.create("resource_tab", **information.get_resource(interaction.user))
        await interaction.response.send_message(view=v, ephemeral=ephemeral)


async def setup(bot: commands.Bot):
    await bot.add_cog(StashCog(bot))