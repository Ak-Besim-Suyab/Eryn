import discord

from cores.logger import logger

from interface.role.image import RoleImage
from interface.role.success import RoleSuccessEmbed

from models.role import role_manager

class RoleThemeEmbed(discord.Embed):
    def __init__(self, interaction: discord.Interaction, category: str, tag: str):
        super().__init__()

        roles = role_manager.get_role_by_tag(tag)

        tincture_description = [
            "> *最後，紋章官僅將符合你使用資格的底色保留在長桌上。*",
            "> *你思索著，並認真地選擇。*",
        ]
        charge_description = [
            "> *最後，紋章官僅將符合你使用資格的徽記保留在長桌上。*",
            "> *你思索著，並認真地選擇。*",
        ]

        descriptions = {
            "tinctures": tincture_description,
            "charges": charge_description
        }

        role_description = []
        for role in roles:
            if role.tag == tag:
                role_description.append(f"- {role.icon}<@&{role.id}>")

        description = "\n".join(descriptions.get(category))

        self.description = description
        self.color = discord.Color.gold()

        self.add_field(name="目前有以下身分組可以套用：", value="\n".join(role_description), inline=False)
        self.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)


class RoleInfo(discord.Embed):
    def __init__(self):
        super().__init__()

        descriptions = [
            "這裡是關於身分組設定的詳細說明，設定時請留意以下規則：",
            "- 徽記身分組的優先級最高，會覆蓋所有其他身分組可能包含的圖案",
            "- 相同分類的身分組同時只能套用 1 個",
        ]

        self.title = "說明"
        self.description = "\n".join(descriptions)
        self.color = discord.Color.gold()


class RoleThemeView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, category: str, tag: str):
        super().__init__(timeout=None)

        self.add_item(RoleThemeOption(category, tag))


class RoleThemeOption(discord.ui.Select):
    def __init__(self, category: str, tag: str):

        self.category = category
        self.tag = tag

        roles = role_manager.get_role_by_tag(tag)

        options = []
        for role in roles:
            if role.tag == self.tag:
                option = discord.SelectOption(
                    label=role.name,
                    value=str(role.id), # 這裡要轉換為字串，因為 SelectOption 的 value 必須是字串類型
                    description="選擇後會套用身分組"
                )
                options.append(option)

        super().__init__(
            placeholder="選擇想要套用的身分組",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        role_id = int(self.values[0])
        selected_role = interaction.guild.get_role(role_id)

        if selected_role is None:
            await interaction.response.send_message("❌ 咪，伺服器找不到該身分組，請回報管理員喵！", ephemeral=True)
            return
        
        if selected_role in interaction.user.roles:
            await interaction.response.send_message("❌ 你已經套用該身分組喵！", ephemeral=True)
            return
        
        try:
            # 移除所有身分組，確保只有一個相同分類的身分組被套用
            roles = role_manager.get_role_by_category(self.category)
            for role in roles:
                removing_role = interaction.guild.get_role(role.id)
                if removing_role in interaction.user.roles:
                    await interaction.user.remove_roles(removing_role)

            await interaction.user.add_roles(selected_role)

            image = RoleImage()
            embed = RoleSuccessEmbed(interaction, role_id)
                
            await interaction.response.send_message(embeds=[image, embed], ephemeral=True)
        except discord.errors.Forbidden:
            await interaction.response.send_message("❌ 出現預期外的錯誤，咪沒有權限套用該身分組... 請聯絡管理員檢查喵！", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("❌ 出現預期外的錯誤，請聯絡管理員檢查喵！", ephemeral=True)
            logger.error(f"使用者套用身分組時發生錯誤：{e}")