import discord
from discord.ext import commands
from discord import app_commands

from database.inventory import Inventory
from database.player import Player

from context import GUILD_TH_HAVEN, GUILD_AK_BESIM, Context


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_shop_data = Context.json_loader.load("data/shop/roles.json")["data"] # type -> list

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="商店", description="開啟商店")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="商店",
            description="請從以下類別中選擇：",
            color=discord.Color.green()
        )
        view = ShopView(self.role_shop_data)
        await interaction.response.send_message(embed=embed, view=view)

# 之後會移到 ui/views/shop_main_view.py
class ShopView(discord.ui.View):
    def __init__(self, role_shop_data):
        super().__init__(timeout=None)
        self.role_shop_data = role_shop_data

    @discord.ui.button(label="身分組", style=discord.ButtonStyle.primary)
    async def role_shop(self, interaction: discord.Interaction, button: discord.ui.Button):

        # 獲取身分組清單，用於印出
        role_list = []
        for role in self.role_shop_data:
            role_list.append(f"<@&{role['role_id']}>")

        embed = discord.Embed(
            title=interaction.user.display_name,
            description=f"你目前有：{Player.get_or_create_player(interaction.user.id).currency} 金幣\n購買身分組後，可以從身分組指令檢視與存取",
            color=discord.Color.green()
        )
        embed.add_field(
            name="身分組列表",
            value="\n".join(role_list),
            inline=False
        )

        view = RoleShopView(interaction, self.role_shop_data)
        await interaction.response.edit_message(embed=embed, view=view)

class RoleShopView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, role_shop_data):
        super().__init__(timeout=None)
        self.role_shop_data = role_shop_data

        # 歷遍身分組，創建購買按鈕
        for role_data in self.role_shop_data:
            button = Button(
                label = f"{role_data['display_name']}：{role_data['price']} 金幣",
                style = discord.ButtonStyle.primary,
                custom_id = f"buy_{role_data['item_id']}",
                role_data = role_data
            )

            # 如果玩家已擁有該身分組，禁用按鈕
            if Inventory.has_item(interaction.user.id, role_data["item_id"]):
                button.disabled = True
                button.style = discord.ButtonStyle.secondary
                button.label = f"{role_data['display_name']}：已擁有"

            self.add_item(button)

class Button(discord.ui.Button):
    def __init__(self, label, style, custom_id, role_data):
        super().__init__(label=label, style=style, custom_id=custom_id)
        self.role_data = role_data

    # buying logic
    async def callback(self, interaction: discord.Interaction):
        
        # 獲取身分組 ID
        player = interaction.user
        role = interaction.guild.get_role(self.role_data["role_id"])
        role_price = self.role_data["price"]
        role_item_id = self.role_data["item_id"]
        role_display_name = self.role_data["display_name"]

        # 確認身分組是否存在
        if not role:
            await interaction.response.send_message("❌ 伺服器內找不到該身分組，請聯絡管理員處理。", ephemeral=True)
            return
        
        # 確認玩家是否已擁有該身分組
        if Inventory.has_item(player.id, role_item_id):
            await interaction.response.send_message(
                f"❌ 你已經擁有{role_display_name}身分組，身分組無法重複購買。",
                ephemeral=True
            )
            return
        
        # 確認玩家是否有足夠金幣
        player_obj = Player.get_or_create_player(player.id)
        if player_obj.currency < role_price:
            await interaction.response.send_message(
                f"❌ 你沒有足夠的金幣購買。",
                ephemeral=True
            )
            return
        
        # 購買身分組
        player_obj.remove_currency(role_price)
        Inventory.add_item(player.id, role_item_id, 1)

        embed = discord.Embed(
            title=interaction.user.display_name,
            description=f"{role_display_name}身分組購買成功，你現在可以在身分組選單自由存取！",
            color=discord.Color.green()
        )
        # 這裡之後改成直接 edit message 然後套用 view 實現類似刷新商店頁面的效果
        # view = ShopView(self.role_shop_data)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Shop(bot))