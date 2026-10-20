import discord
from discord.ext import commands
from discord import app_commands

from cores import logger

from lib import house

class HouseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    house_group = app_commands.Group(
        name="小屋", 
        description="小屋頻道管理的指令叢",
        default_permissions=discord.Permissions(administrator=True))

    list_group = app_commands.Group(
        name="查詢", 
        description="查詢小屋頻道與持有者相關資訊的指令叢",
        parent=house_group
    )

    @house_group.command(name="登記")
    @app_commands.describe(channel="要登記的頻道", member="要登記的成員")
    async def register(self, interaction: discord.Interaction, channel: discord.VoiceChannel, member: discord.Member):

        """為頻道登記持有者，須要提供頻道與成員相關參數。目前預設頻道有唯一持有者，因此若頻道已登記過，將無法再次登記"""

        if not isinstance(channel, discord.VoiceChannel):
            await interaction.response.send_message("提供的頻道似乎不是小屋，請確認頻道類型是否正確", ephemeral=True)
            return 

        registered_house, created = house.register(channel.id, member.id)

        if not created:
            owner = registered_house.owner

            fail_message = f"⚠️ {channel.name}({channel.id}) 已登記在 {owner.display_name}({owner.id}) 名下，無法再次登記。"
            await interaction.response.send_message(fail_message), logger.info(fail_message)
            return

        success_message = f"✅ 成功將 {channel.name}({channel.id}) 登記在 {member.display_name}({member.id}) 名下。"
        await interaction.response.send_message(success_message), logger.info(success_message)

    @house_group.command(name="移除")
    @app_commands.describe(channel="要移除登記的頻道")
    async def delete(self, interaction: discord.Interaction, channel: discord.VoiceChannel):

        """移除頻道登記資訊，須要提供頻道參數"""

        if not isinstance(channel, discord.VoiceChannel):
            await interaction.response.send_message("提供的頻道似乎不是小屋，請確認頻道類型是否正確", ephemeral=True)
            return 

        success = house.delete(channel.id)

        if not success:
            fail_message = f"⚠️ {channel.name}({channel.id}) 尚未登記在任何成員名下，無法移除。"
            await interaction.response.send_message(fail_message), logger.info(fail_message)
            return

        success_message = f"✅ 成功移除 {channel.name}({channel.id}) 的登記資訊。"
        await interaction.response.send_message(success_message), logger.info(success_message)

    @list_group.command(name="已登記成員")
    @app_commands.describe()
    async def list(self, interaction: discord.Interaction):

        """列出所有已登記小屋頻道的持有者"""

        owners = house.get_owners()

        if len(owners) == 0:
            await interaction.response.send_message("目前尚未有任何人登記小屋頻道", ephemeral=True)
            return

        members = [member for member in interaction.guild.members if not member.bot and member.id in owners]

        text = [
            f"已擁有小屋的成員總共： {len(members)} 位。",
            f"已擁有小屋的成員：",
        ]

        for member in members:
            text.append(f"{member.display_name}({member.id})")

        await interaction.response.send_message("已成功列出表單，請查看控制台日誌。", ephemeral=True), logger.info("\n".join(text))

async def setup(bot: commands.Bot):
    await bot.add_cog(HouseCog(bot))