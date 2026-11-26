import discord
from discord.ext import commands
from discord import app_commands

from cogs.inventory import InventoryView
from data.enums import MaterialName, CurrencyName
from lib import player

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
        await interaction.response.send_message(view=InventoryView(interaction.user), ephemeral=ephemeral)

    async def on_resource_tab(self, interaction: discord.Interaction, ephemeral: bool = False):
        await interaction.response.send_message(view=ResourceTabView(interaction), ephemeral=ephemeral)

class ResourceTabView(discord.ui.LayoutView):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)
        
        container = discord.ui.Container()
        container.add_item(get_resource_tab(interaction))
        
        self.add_item(container)

def get_resource_tab(interaction: discord.Interaction) -> discord.ui.TextDisplay:

    # 取得玩家資料
    player_name = interaction.user.display_name

    # 取得通貨
    currencies = player.get_currency(interaction.user.id)

    vin = getattr(currencies, CurrencyName.VIN, 0)

    # 取得材料
    materials = player.get_material(interaction.user.id)

    food  = getattr(materials, MaterialName.FOOD, 0)
    wood  = getattr(materials, MaterialName.WOOD, 0)
    stone = getattr(materials, MaterialName.STONE, 0)
    iron  = getattr(materials, MaterialName.IRON, 0)

    # 組裝內容
    tab = "\n".join(
        [
            f"## {player_name}",
            f"### 通貨",
            f"<:vin:1573407096463163503> **{vin:,}**",
            f"### 材料",
            f"🥩 **{food:,}**",
            f"🪵 **{wood:,}**",
            f"🪨 **{stone:,}**",
            f"<:iron:1573435315522248725> **{iron:,}**"
        ]
    )
    
    return discord.ui.TextDisplay(content=tab)

async def setup(bot: commands.Bot):
    await bot.add_cog(StashCog(bot))