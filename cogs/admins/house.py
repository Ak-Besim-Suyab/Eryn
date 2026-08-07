import discord
from discord.ext import commands
from discord import app_commands
from cores.logger import logger
from systems import house

class AdminHouseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    house = app_commands.Group(
        name="小屋", 
        description="小屋系統頻道管理指令",
        default_permissions=discord.Permissions(administrator=True))

    @house.command(name="登記")
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

    @house.command(name="移除")
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

    @house.command(name="列表")
    @app_commands.describe()
    async def list(self, interaction: discord.Interaction):

        """列出所有已登記的小屋頻道與持有者資訊"""

        owners = house.get_owners()

        if len(owners) == 0:
            await interaction.response.send_message("目前尚未登記任何小屋頻道", ephemeral=True)
            return

        members = [member for member in interaction.guild.members if not member.bot and member.id in owners]

        logger.info(f"目前已擁有小屋的成員總共： {len(members)} 位。")
        logger.info("以下為已擁有小屋的成員：")
        for member in members:
            logger.info(member.display_name)


async def setup(bot: commands.Bot):
    await bot.add_cog(AdminHouseCog(bot))