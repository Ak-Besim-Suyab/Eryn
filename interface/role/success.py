import discord

from models.role import role_manager

class RoleSuccessEmbed(discord.Embed):
    def __init__(self, interaction: discord.Interaction, role_id: int):
        super().__init__()

        role = role_manager.get_role(role_id)

        descriptions = "\n".join([
            "> *你向紋章官申請全新的紋章。*",
            "> *轉眼間，紋章已經遞到你手中。*"
        ])

        self.description = descriptions
        self.color = discord.Color.gold()

        self.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

        self.add_field(name="套用身分組：", value=f"{role.icon}<@&{role_id}>", inline=False)