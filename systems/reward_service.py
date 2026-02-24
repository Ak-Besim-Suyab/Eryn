import discord
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from database.player import Player

from cores.logger import logger

taiwan_timezone = ZoneInfo("Asia/Taipei")

class RewardService:
    async def claim(self, interaction: discord.Interaction):
        # 獲取或創建玩家資料
        player = Player.get_or_create_player(interaction.user.id, interaction.user.display_name)
        # 獲取當前時間
        last_timestamp = player.daily_reward_timestamp
        now_timestamp = time.time()

        if last_timestamp:
            last_datetime = datetime.fromtimestamp(last_timestamp, tz=taiwan_timezone)
            last_date = last_datetime.date()

            now_datetime = datetime.fromtimestamp(now_timestamp, tz=taiwan_timezone)
            now_date = now_datetime.date()
            # 如果玩家上次領取獎勵的日期與今天相同，則無法再次領取
            if now_date <= last_date:
                await interaction.response.send_message("咪！你今天已經領取過每日獎勵了！", ephemeral=True)
                return

        player.daily_reward_timestamp = now_timestamp
        player.add_experience(50)

        stat = player.stats.get()
        stat.total_daily_claims +=1
        stat.save()
        
        embed = discord.Embed(
            title="",
            description="簽到成功，獲得每日獎勵！",
            color=discord.Color.gold()
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="每日獎勵", value="50 經驗值", inline=False)
        embed.add_field(name="累計簽到", value=f"{stat.total_daily_claims} 天", inline=False)
        embed.set_footer(text="咪很開心！每天都要記得來領取獎勵喵！")
        logger.info(f"{player.display_name} 已進行簽到，總天數：{stat.total_daily_claims}")

        await interaction.response.send_message(embed=embed, ephemeral=True)