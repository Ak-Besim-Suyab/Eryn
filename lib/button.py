import discord
import time

from discord import ui

from datetime import datetime

from models import Player
from models import Statistic

from cores import event_bus
from cores import logger

from data.schema.event import ButtonEvent

import data
from lib import builder, information, player

from config import daily_experience
from config import timezone

async def button_attendance_claim(event: ButtonEvent):

    user_id = event.interaction.user.id
    user_name = event.interaction.user.display_name

    last_timestamp = player.get_timestamp_daily(user_id)
    now_timestamp = time.time()

    if last_timestamp:
        last_datetime = datetime.fromtimestamp(last_timestamp, tz=timezone)
        last_date = last_datetime.date()

        now_datetime = datetime.fromtimestamp(now_timestamp, tz=timezone)
        now_date = now_datetime.date()
        
        # 如果玩家上次領取獎勵的日期與今天相同，則無法再次領取
        if now_date <= last_date:
            await event.interaction.response.send_message("咪！你今天已經領取過每日獎勵了！", ephemeral=True)
            return
    
    Player.add_experience(user_id, daily_experience)
    player.set_timestamp_daily(user_id, datetime.now().timestamp())

    stat = Statistic.get_or_create_stat(user_id)
    stat.total_daily_claims +=1
    stat.save()

    embed = discord.Embed()
    embed.description = "簽到成功，獲得每日獎勵！"
    embed.color = discord.Color.gold()
    
    embed.set_author(name=event.interaction.user.display_name, icon_url=event.interaction.user.display_avatar.url)
    embed.add_field(name="每日獎勵", value="50 經驗值", inline=False)
    embed.add_field(name="累計簽到", value=f"{stat.total_daily_claims} 天", inline=False)
    embed.set_footer(text="咪很開心！每天都要記得來領取獎勵喵！")

    await event.interaction.response.send_message(embed=embed, ephemeral=True)

    logger.info(f"{user_name} 已進行簽到，總天數：{stat.total_daily_claims}")

async def button_attendance_guide(event: ButtonEvent):
    view = ui.LayoutView(timeout = None).add_item(builder.build_container(data.container.get("guide_attendance")))
    await event.interaction.response.send_message(view = view, ephemeral = True)

async def button_attendance_information(event: ButtonEvent):
    view = await information.get_information_view(event.interaction)
    await event.interaction.response.send_message(view = view, ephemeral = True)

async def button_attendance_leaderboard(event: ButtonEvent):
    pass
    
async def button_test(event: ButtonEvent):
    await event.interaction.response.send_message("咪，按鈕測試成功發送!", ephemeral=True)

def register():
    event_bus.subscribe(ButtonEvent, "attendance_claim", button_attendance_claim)
    event_bus.subscribe(ButtonEvent, "attendance_guide", button_attendance_guide)
    event_bus.subscribe(ButtonEvent, "attendance_information", button_attendance_information)

    event_bus.subscribe(ButtonEvent, "button_test", button_test)

    logger.info("✅ Button Event Successfully Registered.")