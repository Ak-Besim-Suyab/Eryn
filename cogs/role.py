import discord
from discord.ext import commands
from discord import app_commands

from context import GUILD_TH_HAVEN, GUILD_AK_BESIM, Context
from database.player import Player
from utils.logger import logger

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_data = Context.get_manager("item").get_items_by_tag("role")

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="身分組", description="檢視你可以存取的身分組")
    async def role(self, interaction: discord.Interaction):
        # 這個 player 應該要貫穿整個流程，因此後面都會傳入
        player = Player.get_or_create_player(interaction.user.id)

        embed = discord.Embed(
            title=interaction.user.display_name,
            description="請選擇以下類別檢視身分組。",
            color=discord.Color.green()
        )

        view = RoleView(player, self.role_data)

        await interaction.response.send_message(embed=embed, view=view)

class RoleView(discord.ui.View):
    def __init__(self, player, role_data):
        super().__init__(timeout=None)
        self.player = player
        self.role_data = role_data

    @discord.ui.button(label="顏色身分組", style=discord.ButtonStyle.primary)
    async def color_roles(self, interaction: discord.Interaction, button: discord.ui.Button):

        role_lines = ["目前所有可使用的顏色身分組："]
        for role_id, role_data in self.role_data.items():
            if role_data["flags"].get("is_default") or self.player.has_item(role_id):
                role_lines.append(f"- {role_data.get('emoji_id', '')} <@&{role_data['role_id']}> - *可套用*")
            else:
                role_lines.append(f"- <@&{role_data['role_id']}> - *未擁有*")

        embed = discord.Embed(
            title=interaction.user.display_name,
            description="\n".join(role_lines),
            color=discord.Color.green()
        )

        embed.add_field(
            name="你可以從選單選擇你想要套用的顏色身分組",
            value="備註：顏色身分組同時只能套用 1 個",
            inline=False
        )

        view = RoleSelectView()
        view.add_item(RoleSelector(self.player))
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="圖案身分組", style=discord.ButtonStyle.primary)
    async def pattern_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

class RoleSelectView(discord.ui.View):
    # 這只是個空 view，用來放 select
    def __init__(self):
        super().__init__(timeout=None)

class RoleSelector(discord.ui.Select):
    def __init__(self, player):
        self.player = player
        self.item_manager = Context.get_manager("item")
        self.roles = self.item_manager.get_items_by_tag("role")

        options = []
        for role_name, role_data in self.roles.items():
            # 如果該身分組是預設，或者玩家背包有該身分組道具，則標記為可套用
            if role_data["flags"].get("is_default") or self.player.has_item(role_name):
                options.append(
                    discord.SelectOption(
                        label=f"{role_data['display_name']}",
                        description=f"選擇後會套用身分組",
                        value=role_name
                    )
                )
            else:
                # 如果都沒有，則標記為無法套用
                options.append(
                    discord.SelectOption(
                        label=f"{role_data['display_name']}",
                        description=f"你尚未擁有或解鎖該身分組，無法套用",
                        value=role_name
                    )
                )

        super().__init__(
            placeholder="選擇你想要使用的身分組",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected_role = self.values[0]
        role = self.roles.get(selected_role)
        role_id = role["role_id"]
        guild_role = interaction.guild.get_role(role_id)

        if not guild_role:
            await interaction.response.send_message("❌ 伺服器內找不到該身分組，請聯絡管理員處理。", ephemeral=True)
            return
        
        if guild_role in interaction.user.roles:
            await interaction.response.send_message(f"❌ 你已經套用該身分組。", ephemeral=True)
            return
        
        try:
            # 檢查玩家是否有權限套用此身分組
            is_default = role["flags"].get("is_default", False)
            has_item = self.player.has_item(selected_role)
            
            if not is_default and not has_item:
                await interaction.response.send_message("❌ 你尚未擁有該身分組，無法套用。", ephemeral=True)
                return
            
            # 先加入新身分組
            await interaction.user.add_roles(guild_role, reason="使用者透過指令自行套用身分組。")
            
            # 移除同分類的其他身分組（不移除剛加入的）
            for other_role_name, other_role_data in self.roles.items():
                other_role_id = other_role_data["role_id"]
                # 跳過剛加入的身分組
                if other_role_id == role_id:
                    continue
                
                other_guild_role = interaction.guild.get_role(other_role_id)
                if other_guild_role and other_guild_role in interaction.user.roles:
                    await interaction.user.remove_roles(other_guild_role, reason="機器人系統：顏色身分組同時只能套用 1 個。")
            
            content = f"✅ 成功套用身分組 <@&{role_id}>！"
            await interaction.response.send_message(
                content = content, 
                allowed_mentions=discord.AllowedMentions(roles=False), 
                ephemeral=True
            )

        except discord.Forbidden:
            # 沒有權限時拋出回應
            await interaction.response.send_message("❌ 機器人沒有權限套用該身分組，請聯絡管理員檢查。", ephemeral=True)
            logger.error("機器人沒有權限套用身分組")
            return
        except Exception as e:
            # 其他錯誤時拋出回應
            await interaction.response.send_message("❌ 套用身分組時發生錯誤，請聯絡管理員檢查。", ephemeral=True)
            logger.error(f"套用身分組時發生錯誤：{e}")

async def setup(bot):
    await bot.add_cog(Role(bot))