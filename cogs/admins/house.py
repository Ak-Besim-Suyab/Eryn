import discord
from discord.ext import commands
from cores.logger import logger
from systems import house

class AdminHouseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def house(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            logger.info("使用 !house + 子指令呼叫對應方法")

    @house.command(name="register")
    @commands.is_owner()
    async def register(self, ctx: commands.Context, channel: discord.VoiceChannel, member: discord.Member):

        """為頻道登記持有者，須要提供頻道與成員相關參數。目前預設頻道有唯一持有者，因此若頻道已登記過，將無法再次登記"""

        if not isinstance(channel, discord.VoiceChannel):
            await ctx.send("提供的頻道似乎不是小屋，請確認頻道類型是否正確")
            return 

        registered_house, created = house.register(channel.id, member.id)

        if not created:
            owner = registered_house.owner

            fail_message = f"⚠️ {channel.name}({channel.id}) 已登記在 {owner.display_name}({owner.id}) 名下，無法再次登記。"
            await ctx.send(fail_message), logger.info(fail_message)
            return

        success_message = f"✅ 成功將 {channel.name}({channel.id}) 登記在 {member.display_name}({member.id}) 名下。"
        await ctx.send(success_message), logger.info(success_message)

    @house.command(name="delete")
    @commands.is_owner()
    async def delete(self, ctx: commands.Context, channel: discord.VoiceChannel):

        """刪除頻道登記資訊，須要提供頻道參數"""

        if not isinstance(channel, discord.VoiceChannel):
            await ctx.send("提供的頻道似乎不是小屋，請確認頻道類型是否正確")
            return 

        success = house.delete(channel.id)

        if not success:
            fail_message = f"⚠️ {channel.name}({channel.id}) 尚未登記在任何成員名下，無法刪除。"
            await ctx.send(fail_message), logger.info(fail_message)
            return

        success_message = f"✅ 成功刪除 {channel.name}({channel.id}) 的登記資訊。"
        await ctx.send(success_message), logger.info(success_message)

    @house.command(name="list")
    @commands.is_owner()
    async def list(self, ctx: commands.Context):

        """列出所有已登記的小屋頻道與持有者資訊"""

        owners = house.get_owners()

        if len(owners) == 0:
            await ctx.send("目前尚未登記任何小屋頻道")
            return

        members = [member for member in ctx.guild.members if not member.bot and member.id in owners]

        logger.info(f"目前已擁有小屋的成員總共： {len(members)} 位。")
        logger.info("以下為已擁有小屋的成員：")
        for member in members:
            logger.info(member.display_name)


async def setup(bot: commands.Bot):
    await bot.add_cog(AdminHouseCog(bot))