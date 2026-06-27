import discord
from discord.ext import commands

from cores import logger
from utils import time

notice_channel_id = 1198867692497674241

class MemberEventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        if member.bot:
            return
        
        embed = self.get_embed("member_join", member)
        
        notice_channel = self.bot.get_channel(notice_channel_id)
        if notice_channel is not None:
            await notice_channel.send(embed=embed)
        else:
            logger.error("找不到通知頻道")

        logger.info(f"{member.id} | {member.name} | {member.display_name} 剛剛加入了群組。")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):

        if member.bot:
            return
        
        embed = self.get_embed("member_remove", member)

        notice_channel = self.bot.get_channel(notice_channel_id)
        if notice_channel is not None:
            await notice_channel.send(embed=embed)
        else:
            logger.error("找不到通知頻道")

        logger.info(f"{member.id} | {member.name} | {member.display_name} 剛剛離開了群組。")

#--------------------------------------------------------

    def get_embed(self, event_type: str, member: discord.Member) -> discord.Embed:

        descriptions = {
            "member_join": f"<@{member.id}> (ID:{member.id}) 加入群組",
            "member_remove": f"<@{member.id}> (ID:{member.id}) 離開群組",
        }

        colors = {
            "member_join": discord.Color.green(),
            "member_remove": discord.Color.red(),
        }

        now = time.get_formatted_time()

        embed = discord.Embed()
        embed.color = colors.get(event_type)
        embed.description = descriptions.get(event_type)

        embed.add_field(name="成員資訊", value=self.get_info(member), inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"成員總數：{member.guild.member_count} {now}")

        return embed

    def get_info(self, member: discord.Member) -> str:
        info = []

        info.append(f"帳號名稱：*{member.name}*")
        info.append(f"顯示名稱：*{member.display_name}*")

        return "\n".join(info)

async def setup(bot: commands.Bot):
    await bot.add_cog(MemberEventCog(bot))