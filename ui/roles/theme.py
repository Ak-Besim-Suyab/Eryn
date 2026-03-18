import discord

from cores.loader import JsonLoader
from cores.logger import logger

class RoleThemeEmbed(discord.Embed):
    def __init__(self, interaction: discord.Interaction, category: str, group: str):
        super().__init__()

        roles = JsonLoader.load(f"data/roles/{category}.json")

        role_description = []
        for role in roles:
            role_group = role.get("group")
            if role_group == group:
                role_id = role.get("role_id")
                role_image = role.get("role_image")

                role_description.append(f"- <@&{role_id}>{role_image} - *可套用*")

        self.color = discord.Color.gold()
        self.add_field(name="選擇以下身分組進行套用：", value="\n".join(role_description), inline=False)
        self.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)


class RoleInfoEmbed(discord.Embed):
    def __init__(self):
        super().__init__()

        descriptions = [
            "> 這裡是關於身分組設定的詳細說明，設定時請留意以下規則：",
            "> - 徽記身分組的優先級最高，會覆蓋所有其他身分組可能包含的圖案",
            "> - 相同分類的身分組同時只能套用 1 種",
        ]

        self.title = "說明"
        self.description = "\n".join(descriptions)
        self.color = discord.Color.gold()


class RoleThemeView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, category: str, group: str):
        super().__init__(timeout=None)

        self.add_item(RoleThemeOption(category, group))


class RoleThemeOption(discord.ui.Select):
    def __init__(self, category: str, group: str):

        self.category = category
        self.group = group
        self.roles = JsonLoader.load(f"data/roles/{category}.json")

        options = []
        for role in self.roles:
            role_group = role.get("group")
            if role_group == group:
                role_id = role.get("role_id")
                role_name = role.get("role_name")
                description = "選擇後會套用身分組"

                option = discord.SelectOption(label=role_name, description=description, value=role_id)
                options.append(option)

        super().__init__(
            placeholder="選擇想要套用的身分組",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        selected_role = interaction.guild.get_role(int(self.values[0]))

        if not selected_role:
            await interaction.response.send_message("❌ 咪，伺服器找不到該身分組，請聯絡管理員處理。", ephemeral=True)
            logger.error(f"使用者所選擇的身分組未在伺服器內找到：{self.values[0]}")
            return
        
        if selected_role in interaction.user.roles:
            await interaction.response.send_message(f"❌ 你已經套用該身分組。", ephemeral=True)
            return
        
        try:
            # 移除所有身分組，確保只有一個相同分類的身分組被套用
            for role in self.roles:
                removing_role = interaction.guild.get_role(role.get("role_id"))
                if removing_role in interaction.user.roles:
                    await interaction.user.remove_roles(removing_role)

            await interaction.user.add_roles(selected_role)
                
            await interaction.response.send_message(f"✅ 成功套用身分組：<@&{self.values[0]}>", ephemeral=True)
        except discord.errors.Forbidden:
            await interaction.response.send_message("❌ 沒有權限套用該身分組。", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("❌ 出現預期外的錯誤，請聯絡管理員檢查與處理。", ephemeral=True)
            logger.error(f"使用者套用身分組時發生錯誤：{e}")