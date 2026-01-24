import json
import discord
from discord import app_commands
from discord.ext import commands

from database.inventory import Inventory
from utils.logger import logger
from utils.file_loader import JsonLoader
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM


json_loader = JsonLoader()


class ShopRoleData:
    def __init__(self, json_path: str = "data/shop_roles.json"):
        self.roles = []
        self._load_from_json(json_path)

    def _load_from_json(self, json_path: str):
        data = json_loader.load(json_path)
        if data:
            self.roles = data.get('roles', [])
            logger.info(f"[身分組] 載入 {len(self.roles)} 個身分組")
        else:
            logger.error(f"[身分組] 找不到檔案或讀取失敗：{json_path}")
            self.roles = []

    def get_all_roles(self) -> list:
        return self.roles

    def get_role_by_id(self, role_id: int) -> dict:
        for role in self.roles:
            if role['role_id'] == role_id:
                return role
        return None


class RoleSelectView(discord.ui.View):
    def __init__(self, roles: list, member: discord.Member):
        super().__init__(timeout=180)
        self.roles = roles
        self.member = member
        self._add_role_buttons()

    def _add_role_buttons(self):
        if not self.roles:
            no_role_button = discord.ui.Button(
                label="沒有已購買的身分組",
                style=discord.ButtonStyle.secondary,
                disabled=True
            )
            self.add_item(no_role_button)
            return

        for role_data in self.roles:
            button = discord.ui.Button(
                label=role_data['name'],
                style=discord.ButtonStyle.primary,
                custom_id=f"apply_role_{role_data['role_id']}"
            )
            button.callback = self._make_apply_callback(role_data)
            self.add_item(button)

    def _make_apply_callback(self, role_data: dict):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.member.id:
                await interaction.response.send_message("❌ 只能由本人操作此選單", ephemeral=True)
                return

            qty = Inventory.get_quantity(self.member.id, role_data['item_id'])
            if qty < 1:
                await interaction.response.send_message("❌ 你尚未購買此身分組", ephemeral=True)
                return

            guild_role = interaction.guild.get_role(role_data['role_id']) if interaction.guild else None
            if not guild_role:
                await interaction.response.send_message("❌ 找不到該身分組，請聯繫管理員", ephemeral=True)
                logger.error(f"[身分組] 找不到身分組 ID: {role_data['role_id']}")
                return

            if guild_role in interaction.user.roles:
                await interaction.response.send_message(
                    f"ℹ️ 你已套用 **{role_data['name']}**",
                    ephemeral=True
                )
                return

            try:
                await interaction.user.add_roles(guild_role, reason="玩家選擇套用身分組")
            except discord.Forbidden:
                await interaction.response.send_message("❌ 機器人沒有權限授予身分組", ephemeral=True)
                logger.error(f"[身分組] 機器人無權限授予身分組 {role_data['role_id']}")
                return
            except Exception as e:
                await interaction.response.send_message(f"❌ 套用失敗：{e}", ephemeral=True)
                logger.error(f"[身分組] 套用身分組失敗：{e}")
                return

            embed = self.build_owned_role_embed(interaction.user)
            await interaction.response.edit_message(embed=embed, view=self)
            # 額外顯示該身分組的詳細 embed 含顏色
            detail_embed = self.build_role_detail_embed(role_data, interaction.user)
            await interaction.followup.send(embed=detail_embed, ephemeral=True)

        return callback

    def build_owned_role_embed(self, member: discord.Member) -> discord.Embed:
        embed = discord.Embed(
            title="🎭 套用身分組",
            description="選擇你已購買的身分組進行套用。",
            color=discord.Color.purple()
        )

        added_field = False
        for role_data in self.roles:
            guild_role = member.guild.get_role(role_data['role_id']) if member.guild else None
            if not guild_role:
                continue
            status = "✅ 已套用" if guild_role in member.roles else "未套用"
            # 使用身分組的顏色來顯示
            role_color = guild_role.color if guild_role.color != discord.Color.default() else discord.Color.purple()
            embed.add_field(
                name=f"{role_data['name']}",
                value=f"{role_data['description']}\n**{status}**",
                inline=False
            )
            added_field = True

        if not added_field:
            embed.description = "你尚未購買任何身分組，請先使用 /商店 購買。"

        return embed

    def build_role_detail_embed(self, role_data: dict, member: discord.Member) -> discord.Embed:
        """為單一身分組建立詳細 embed，使用該身分組的顏色"""
        guild_role = member.guild.get_role(role_data['role_id']) if member.guild else None
        role_color = guild_role.color if guild_role and guild_role.color != discord.Color.default() else discord.Color.purple()
        
        embed = discord.Embed(
            title=f"已套用身分組",
            description=role_data['description'],
            color=role_color
        )
        
        # 用提及格式直接顯示身分組的顏色和名稱
        embed.add_field(
            name="身分組",
            value=f"<@&{role_data['role_id']}>",
            inline=False
        )
        
        return embed


class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="身分組", description="選擇已購買的身分組並套用")
    async def role_select_command(self, interaction: discord.Interaction):
        shop_data = ShopRoleData()
        member = interaction.user

        available_roles = []
        for role_data in shop_data.get_all_roles():
            if Inventory.get_quantity(member.id, role_data['item_id']) < 1:
                continue
            if not interaction.guild:
                continue
            guild_role = interaction.guild.get_role(role_data['role_id'])
            if not guild_role:
                logger.error(f"[身分組] 找不到身分組 ID: {role_data['role_id']}")
                continue
            available_roles.append(role_data)

        if not available_roles:
            await interaction.response.send_message("❌ 你尚未購買任何身分組，請先使用 /商店 購買。", ephemeral=True)
            return

        view = RoleSelectView(available_roles, member)
        embed = view.build_owned_role_embed(member)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Role(bot))
