import json
import discord
from discord import app_commands
from discord.ext import commands

from database.player import Player
from database.inventory import Inventory
from cogs.inventory import build_inventory_embed, InventoryActionView
from utils.logger import logger
from utils.embed_builder import EmbedBuilder
from utils.file_loader import JsonLoader
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM


embed_builder = EmbedBuilder()
json_loader = JsonLoader()


class ShopRoleData:
    def __init__(self, json_path: str = "data/shop_roles.json"):
        self.roles = []
        self._load_from_json(json_path)

    def _load_from_json(self, json_path: str):
        data = json_loader.load(json_path)
        if data:
            self.roles = data.get('roles', [])
            logger.info(f"[商店] 載入 {len(self.roles)} 個身分組商品")
        else:
            logger.error(f"[商店] 找不到檔案或讀取失敗：{json_path}")
            self.roles = []

    def get_all_roles(self) -> list:
        return self.roles

    def get_role_by_id(self, role_id: int) -> dict:
        for role in self.roles:
            if role['role_id'] == role_id:
                return role
        return None


class ShopMainView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="身分組", style=discord.ButtonStyle.primary, emoji="🎭")
    async def role_shop(self, interaction: discord.Interaction, button: discord.ui.Button):
        shop_data = ShopRoleData()
        view = RoleShopView(shop_data)
        embed = view.build_role_shop_embed(interaction.user.id, interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="返回", style=discord.ButtonStyle.secondary, emoji="◀️")
    async def back_to_inventory(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = build_inventory_embed(interaction.user)
        await interaction.response.edit_message(
            embed=embed,
            view=InventoryActionView()
        )


class RoleShopView(discord.ui.View):
    def __init__(self, shop_data: ShopRoleData):
        super().__init__(timeout=None)
        self.shop_data = shop_data
        self._add_role_buttons()

    def _add_role_buttons(self):
        """添加身分組購買按鈕和返回按鈕"""
        for role in self.shop_data.get_all_roles():
            button = discord.ui.Button(
                label=role['name'],
                emoji=role['emoji'],
                style=discord.ButtonStyle.primary,
                custom_id=f"buy_role_{role['role_id']}",
                row=0
            )
            button.callback = self._create_purchase_callback(role)
            self.add_item(button)

        back_button = discord.ui.Button(
            label="返回",
            style=discord.ButtonStyle.secondary,
            emoji="◀️",
            row=1
        )
        back_button.callback = self._back_to_shop
        self.add_item(back_button)

    def build_role_shop_embed(self, user_id: int, guild: discord.Guild) -> discord.Embed:
        embed = embed_builder.create("shop_role_header")[0]

        for role in self.shop_data.get_all_roles():
            item_id = role['item_id']
            quantity = Inventory.get_quantity(user_id, item_id)
            is_purchased = quantity >= 1

            status = "✓ 已購買" if is_purchased else f"💰 {role['price']} 金幣"

            embed.add_field(
                name=f"{role['emoji']} {role['name']}",
                value=f"<@&{role['role_id']}>\n{status}",
                inline=True
            )

        return embed

    def _create_purchase_callback(self, role_data: dict):
        async def callback(interaction: discord.Interaction):
            player_id = interaction.user.id
            item_id = role_data['item_id']
            role_id = role_data['role_id']
            price = role_data['price']

            quantity = Inventory.get_quantity(player_id, item_id)
            if quantity >= 1:
                await interaction.response.send_message("❌ 你已經購買過此身分組", ephemeral=True)
                return

            player = Player.get_or_create_player(player_id)
            if player.currency_yab < price:
                await interaction.response.send_message(
                    f"❌ 金幣不足！需要 {price} 金幣，你目前有 {player.currency_yab} 金幣",
                    ephemeral=True
                )
                return

            try:
                role = interaction.guild.get_role(role_id)
                if not role:
                    await interaction.response.send_message("❌ 找不到該身分組，請聯繫管理員", ephemeral=True)
                    logger.error(f"[商店] 找不到身分組 ID: {role_id}")
                    return

                Player.decrease_currency(player_id, price)
                Inventory.add_item(player_id, item_id, 1)
                await interaction.user.add_roles(role, reason="從商店購買")

                await interaction.response.send_message(
                    f"✅ 成功購買 {role_data['emoji']} **{role_data['name']}** 身分組！\n花費 {price} 金幣\n\n已套用身分組：<@&{role_id}>",
                    ephemeral=True
                )
                logger.info(f"[商店] {interaction.user} 購買了 {role_data['name']} 身分組")

                embed = self.build_role_shop_embed(player_id, interaction.guild)
                await interaction.message.edit(embed=embed, view=self)

            except discord.Forbidden:
                await interaction.response.send_message("❌ 機器人沒有權限授予身分組", ephemeral=True)
                logger.error(f"[商店] 機器人無權限授予身分組 {role_id}")
            except Exception as e:
                await interaction.response.send_message(f"❌ 購買失敗：{e}", ephemeral=True)
                logger.error(f"[商店] 購買身分組失敗：{e}")

        return callback

    async def _back_to_shop(self, interaction: discord.Interaction):
        """返回商店主頁"""
        view = ShopMainView()
        embed = embed_builder.create("shop_main_page")[0]
        await interaction.response.edit_message(
            embed=embed,
            view=view
        )

    def _build_shop_embed(self) -> discord.Embed:
        """構建身分組商店頁面基礎 embed"""
        return embed_builder.create("shop_role_header")[0]


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="商店", description="瀏覽商店並購買物品")
    async def shop_command(self, interaction: discord.Interaction):
        view = ShopMainView()
        embed = embed_builder.create("shop_main_page")[0]
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Shop(bot))
