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
                label=role_data.name,
                emoji=role_data.icon,
                value=role_data.id,
            )
            for role_data in roles
        ]

        super().__init__(
            placeholder=placeholder,
            custom_id=custom_id,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if interaction.guild is None or not isinstance(interaction.user, discord.Member):
            await interaction.followup.send("❌ 此功能僅限在伺服器內使用。", ephemeral=True)
            return

        role_data = ROLES.get(self.values[0])
        if role_data is None:
            await interaction.followup.send("❌ 發生錯誤，找不到該身分組設定，請回報管理員！", ephemeral=True)
            return

        selected_role = interaction.guild.get_role(role_data.discord_id)
        if selected_role is None:
            await interaction.followup.send("❌ 發生錯誤，該身分組似乎不存在，請回報管理員！", ephemeral=True)
            return

        try:
            # 取得相同分類的身分組資料，用於檢查唯一身分組
            category_roles = ROLES.find(category=role_data.category)
            category_role_ids = {r.discord_id for r in category_roles}

            # 取得要移除的其他同類身分組
            removing_roles = [r for r in interaction.user.roles if r.id in category_role_ids]

            # 移除其他同類身分組，接著套用新的身分組
            if removing_roles:
                await interaction.user.remove_roles(*removing_roles, reason="套用唯一身分組，移除其他相同分類身分組")
            await interaction.user.add_roles(selected_role, reason="使用下拉式選單套用身分組")

            await interaction.followup.send("✅ 身分組套用成功，在社群頻道裡查看您的外觀吧！", ephemeral=True)
        except discord.errors.Forbidden:
            await interaction.followup.send(
                "❌ 出現預期外的錯誤，咪沒有權限套用該身分組... 請管理員檢查權限！",
                ephemeral=True,
            )
        except Exception as e:
            await interaction.followup.send("❌ 出現預期外的錯誤，請管理員檢查日誌！", ephemeral=True)
            logger.exception(f"使用者套用身分組時發生錯誤：{e}")
