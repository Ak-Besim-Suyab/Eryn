"""
該類別主要用來監聽語音事件，當成員加入或離開語音頻道時，會在指定的頻道發送通知訊息，並且記錄成員的語音經驗值。
"""

import discord
from discord.ext import commands

from game.systems import LevelSystem

from cores import logger
from utils import time

notice_channel_id = 1198867692497674241

class VoiceListener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):

        # 忽略機器人進出語音
        if member.bot:
            return
        
        # 語音狀態檢查
        if after.channel and not before.channel:

            await self.send("enter_voice", member, after.channel)

            LevelSystem.save_timestamp(member)
            
        elif before.channel and not after.channel:

            await self.send("leave_voice", member, before.channel)

            LevelSystem.give_voice_experience(member)
            LevelSystem.remove_timestamp(member)


    async def send(self, type: str, member: discord.Member, channel: discord.VoiceChannel):

        notice_channel = self.bot.get_channel(notice_channel_id)
        if notice_channel is not None:
            embed = await self.get_embed(type, member, channel)
            await notice_channel.send(embed=embed)
        else:
            logger.error("找不到通知頻道")
    
    
    async def get_embed(self, event_type: str, member: discord.Member, channel: discord.VoiceChannel) -> discord.Embed:

        descriptions = {
            "enter_voice": f"<@{member.id}> 加入了語音頻道：`{channel.name}`",
            "leave_voice": f"<@{member.id}> 離開了語音頻道：`{channel.name}`",
        }

        log_descriptions = {
            "enter_voice": f"{member.display_name} ({member.id}) 加入了語音頻道：{channel.name}",
            "leave_voice": f"{member.display_name} ({member.id}) 離開了語音頻道：{channel.name}",
        }

        now = time.get_formatted_time()

        embed = discord.Embed()
        embed.color = discord.Color.gold()
        embed.description = descriptions.get(event_type)

        embed.set_footer(text=now)
        embed.set_author(name=member.name, icon_url=member.avatar.url)

        logger.info(log_descriptions.get(event_type))

        return embed

async def setup(bot):
    await bot.add_cog(VoiceListener(bot))