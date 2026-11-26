import discord

from data import ROLES

from lib import role

class RoleSelect(discord.ui.Select):
    def __init__(self, custom_id: str, placeholder: str = "選擇想套用的身分組", **filters):
        
        roles = ROLES.find(**filters)
        if not roles:
            raise ValueError(f"找不到符合條件 {filters} 的身分組，無法建立選單")

        options = [
            discord.SelectOption(label=r.display_name, emoji=r.emoji, value=str(r.id))
            for r in roles
        ]

        super().__init__(
            placeholder=placeholder,
            custom_id=custom_id,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if not isinstance(interaction.user, discord.Member):
            await interaction.followup.send("❌ 此功能僅限在伺服器中使用！", ephemeral=True)
            return

        message = await role.switch(interaction.user, int(self.values[0]))
        await interaction.followup.send(message, ephemeral=True)
