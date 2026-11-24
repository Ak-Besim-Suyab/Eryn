import discord

from cores import logger
from data import ROLES

class RoleSelect(discord.ui.Select):
    def __init__(self, custom_id: str, placeholder: str = "選擇想套用的身分組", **filters):
        
        roles = ROLES.find(**filters)
        if not roles:
            raise ValueError(f"找不到符合條件 {filters} 的身分組，無法建立選單")

        options = [
            discord.SelectOption(
                label=role.display_name,
                emoji=role.emoji,
                value=role.display_name,
            )
            for role in roles
        ]

        super().__init__(
            placeholder=placeholder,
            custom_id=custom_id,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        
        await interaction.response.defer(ephemeral=True)

        # 取得身分組資料
        role = ROLES.find(display_name=self.values[0])[0]
        if role is None:
            await interaction.followup.send("❌ 發生錯誤，找不到身分組資料！", ephemeral=True)
            return

        # 取得身分組物件
        selected_role = interaction.guild.get_role(role.id)
        if selected_role is None:
            await interaction.followup.send("❌ 發生錯誤，身分組不存在！", ephemeral=True)
            return

        try:
            # 取得相同分類的身分組資料
            category_role_ids = {role.id for role in ROLES.find(category=role.category)}

            # 取得要移除的其他同類身分組
            removing_roles = [role for role in interaction.user.roles if role.id in category_role_ids]

            # 移除其他同類身分組
            if removing_roles:
                await interaction.user.remove_roles(*removing_roles, reason="套用唯一身分組，移除其他相同分類身分組")
            
            # 套用新的身分組
            await interaction.user.add_roles(selected_role, reason="使用下拉式選單套用身分組")

            await interaction.followup.send("✅ 身分組套用成功，在社群頻道裡查看您的外觀吧！", ephemeral=True)

        except discord.errors.Forbidden:
            logger.error(f"無法套用身分組 {selected_role.name} 給使用者 {interaction.user.name}，權限不足")
            
        except Exception as e:
            logger.error(f"使用者套用身分組時發生錯誤：{e}")
