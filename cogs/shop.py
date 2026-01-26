import discord
from discord.ext import commands
from discord import app_commands

from database.inventory import Inventory
from database.player import Player

from context import GUILD_TH_HAVEN, GUILD_AK_BESIM

# @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
# class ShopGroup(app_commands.Group):
#     def __init__(self):
#         super().__init__(name = "商店", description = "購買道具")

#     @app_commands.command(name="身分組", description="購買獨特身分組")
#     async def role_shop(self, interaction: discord.Interaction):
#         pass

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="商店", description="開啟商店")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="商店",
            description="請從以下類別中選擇：",
            color=discord.Color.green()
        )
        view = ShopView()
        await interaction.response.send_message(embed=embed, view=view)

# 之後會移到 ui/views/shop_main_view.py
class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="身分組", style=discord.ButtonStyle.primary)
    async def role_shop(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="身分組商店",
            description=f"你目前有：{Player.get_or_create_player(interaction.user.id).currency_yab} 金幣\n當你購買身分組後，可以從 /身分組 檢視清單並自由存取",
            color=discord.Color.green()
        )
        embed.add_field(
            name="重飽和色系列",
            value="<@&1460042229425901682> \n<@&1460037724437483614>",
            inline=False
        )

        view = RoleShopView()
        await interaction.response.edit_message(embed=embed, view=view)

class RoleShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def buy_role(self, interaction, role_name, price):
        player = Player.get_or_create_player(interaction.user.id)
        role = interaction.guild.get_role(role_name)

        role_ids = {
            "role_crimson": 1460042229425901682,
            "role_abyss": 1460037724437483614
        }

        # 確認身分組是否存在
        if not role:
            await interaction.response.send_message(
                "❌ 伺服器內找不到該身分組，請聯絡管理員。",
                ephemeral=True
            )
            return
        
        # 確認玩家是否有足夠金幣
        if player.currency_yab < price:
            await interaction.response.send_message(
                f"❌ 你沒有足夠的金幣購買身分組，價格為 {price} 金幣。",
                ephemeral=True
            )
            return
        
        # 購買身分組
        Player.decrease_currency(player.id, price)
        Inventory.add_item(player.id, role_ids[role_name], 1)

    @discord.ui.button(label="購買 緋紅", style=discord.ButtonStyle.primary)
    async def buy_crimson_role(self, interaction: discord.Interaction, button: discord.ui.Button):

        await self.buy_role(interaction, "role_crimson", 500)

        embed = discord.Embed(
            title=interaction.user.display_name,
            description=f"緋紅身分組購買成功，你現在可以在身分組選單自由存取！",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="購買 深淵", style=discord.ButtonStyle.primary)
    async def buy_abyss_role(self, interaction: discord.Interaction, button: discord.ui.Button):

        await self.buy_role(interaction, "role_abyss", 500)

        embed = discord.Embed(
            title=interaction.user.display_name,
            description=f"深淵身分組購買成功，你現在可以在身分組選單自由存取！",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

# class Shop(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.bot.tree.add_command(ShopGroup())

async def setup(bot):
    await bot.add_cog(Shop(bot))