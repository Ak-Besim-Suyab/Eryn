import discord
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from models.player import Player
from models.message import message_manager
from cores.logger import logger


taiwan_timezone = ZoneInfo("Asia/Taipei")

class RewardService:
    async def claim(self, interaction: discord.Interaction):

        daily_experience = 100

        user_id = interaction.user.id

        last_timestamp = Player.get_timestamp_daily_reward(user_id)
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

        Player.save_timestamp_daily_reward(user_id)
        Player.add_experience(user_id, daily_experience)

        stat = Player.get_stat(user_id)
        stat.total_daily_claims +=1
        stat.save()
        
        payload = {
            "experience": daily_experience,
            "total_daily_claims": stat.total_daily_claims
        }

        logger.info(f"{interaction.user.display_name} 已進行簽到，總天數：{stat.total_daily_claims}")

        return payload