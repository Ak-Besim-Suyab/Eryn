import discord

from database.player import Player

from ui.views.role_menu_view import RoleMenuView
from ui.views.role_option_view import RoleOptionView

from ui.components.role_option import RoleOption
from ui.components.role_menu_option import RoleMenuOption

from context import Context

class RoleSession:
    def __init__(self):
        self.role_menu_view = RoleMenuView()
        self.role_option_view = RoleOptionView(self)

    async def start(self, interaction: discord.Interaction):

        for child in self.role_menu_view.children[:]:
            if isinstance(child, discord.ui.Select):
                self.role_menu_view.remove_item(child)

        embed = discord.Embed(
            title=interaction.user.display_name,
            description="請選擇以下類別檢視身分組。",
            color=discord.Color.gold()
        )
        self.role_menu_view.add_item(RoleMenuOption(self))
        await interaction.response.send_message(embed=embed, view=self.role_menu_view)

    async def render_role_option(self, interaction: discord.Interaction, role_tag, category_tag = "default"):

        player = Player.get_or_create_player(interaction.user.id)

        # 由於 RoleOptionView 會複用，因此需要清空舊的 RoleOption 避免殘留的選項被輸出
        for child in self.role_option_view.children[:]:
            if isinstance(child, discord.ui.Select):
                self.role_option_view.remove_item(child)

        # 將標籤轉為 list 並清除空值，接著調用 get_items_by_tag 獲取身分組資料
        tags = [tag for tag in [role_tag, category_tag] if tag != "default"]
        role_data = Context.get_manager("item").get_items_by_tag(tags)
        
        if not role_data:
            embed = discord.Embed(
                title=interaction.user.display_name,
                description="目前尚未擁有任何可以套用的身分組。",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=self.role_option_view)
            return

        # 印出身分組清單
        role_lines = []
        for role_id, data in role_data.items():
            emoji = data.get("emoji_id", "")
            flags = data.get("flags", {})

            if flags.get("is_default") or player.has_item(role_id):
                role_lines.append(f"- <@&{data['role_id']}>{emoji} - *可套用*")
            else:
                role_lines.append(f"- <@&{data['role_id']}>{emoji} - *未擁有*")

        embed = discord.Embed(
            title=f"{interaction.user.display_name}可套用的身分組",
            description="\n".join(role_lines),
            color=discord.Color.gold()
        )

        manual = [
            "你可以從下方選擇想要套用的身分組",
            "> - 圖案身分組優先級最高，會覆蓋所有身分組圖案",
            "> - 相同分類的身分組同時只能套用 1 個",
            "> - 特定身分組需要遊玩遊戲才能解鎖",
        ]

        embed.add_field(
            name="說明：",
            value="\n".join(manual),
            inline=False
        )

        self.role_option_view.add_item(RoleOption(self, player, role_tag, role_data))
        await interaction.response.edit_message(embed=embed, view=self.role_option_view)