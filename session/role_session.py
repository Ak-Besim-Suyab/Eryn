import discord

from database.player import Player

from ui.views.role_menu_view import RoleMenuView
from ui.views.role_option_view import RoleOptionView

from ui.components.role_option import RoleOption

from context import Context

class RoleSession:
    def __init__(self):
        self.role_menu_view = RoleMenuView(self)
        self.role_option_view = RoleOptionView(self)
        self.manager = Context.get_manager("item")

    async def start(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=interaction.user.display_name,
            description="請選擇以下類別檢視身分組。",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, view=self.role_menu_view)

    async def render_role(self, role_type: str, interaction: discord.Interaction):
        """
        role_type will be only: color_role, icon_role
        """
        branch = {
            "color_role": "顏色身分組",
            "icon_role": "圖案身分組"
        }
        player = Player.get_or_create_player(interaction.user.id)

        role_data = self.manager.get_items_by_tag(role_type)
        # 如果沒有任何符合標籤的身分組，不往下執行，回傳訊息，避免 select 因為沒有產生選項報錯
        if not role_data:
            embed = discord.Embed(
                title=f"{interaction.user.display_name}的{branch[role_type]}",
                description="目前沒有可用的身分組。",
                color=discord.Color.gold()
            )
            await interaction.response.edit_message(embed=embed, view=self.role_option_view)
            return

        role_lines = []
        for role_id, data in role_data.items():
            emoji = data.get("emoji_id", "")
            flags = data.get("flags", {})

            if flags.get("is_default") or player.has_item(role_id):
                role_lines.append(f"- {emoji}<@&{data['role_id']}> - *可套用*")
            else:
                role_lines.append(f"- {emoji}<@&{data['role_id']}> - *未擁有*")

        # Create the embed message
        embed = discord.Embed(
            title=f"{interaction.user.display_name}的{branch[role_type]}",
            description="\n".join(role_lines),
            color=discord.Color.gold()
        )

        # Add explanation field
        embed.add_field(
            name="說明：",
            value=f"你可以從下方選擇你想要套用的{branch[role_type]}\n> 備註：{branch[role_type]}同時只能套用 1 個",
            inline=False
        )

        view = discord.ui.View() # Empty view to hold options
        view.add_item(RoleOption(self, player, role_data))
        await interaction.response.edit_message(embed=embed, view=view)