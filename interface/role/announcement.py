import discord
import asyncio

from interface.role.image import RoleImage, image_college_of_arms
from interface.role.main import RoleEmbed, RoleView

class RoleAnnouncementEmbed(discord.Embed):
    def __init__(self):
        super().__init__()
        description = "\n".join([
            "> 前往紋章院，定製你的獨特紋章（身分組）",
        ])

        self.title = "紋章院（College of Arms）"
        self.description = description
        self.color = discord.Color.gold()

        self.set_image(url=image_college_of_arms)

class RoleAnnouncementView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="前往", style=discord.ButtonStyle.primary, custom_id="role_setting")
    async def trade(self, interaction: discord.Interaction, button: discord.ui.Button):
        image = RoleImage()
        embed = RoleEmbed()
        view = RoleView()
        await interaction.response.send_message(embeds=[image, embed], view=view, ephemeral=True)

    @discord.ui.button(label="這是什麼？", style=discord.ButtonStyle.secondary, custom_id="role_setting_help")
    async def help(self, interaction: discord.Interaction, button: discord.ui.Button):
        descriptions = [
            "「咪，這裡是全新的身分組設定系統，旅人可以透過這個系統選擇與搭配屬於自己的獨特身分組！」",
            "「關於系統的詳細說明，過程中都會提供指示；如果使用過程中出現任何錯誤，或是有任何建議，都歡迎回報給管理員！」",
        ]
        embed = discord.Embed()
        embed.title = "Elin"
        embed.color = discord.Color.gold()
        embed.set_thumbnail(url=interaction.client.user.avatar.url)

        await interaction.response.defer(ephemeral=True)

        for description in descriptions:

            embed.description = description

            async with interaction.channel.typing():
                await asyncio.sleep(3)

            await interaction.followup.send(embed=embed, ephemeral=True)