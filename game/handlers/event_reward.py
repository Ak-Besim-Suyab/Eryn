"""
此類別為獎勵系統，這裡會負責處理大部分與 Player 數據有關的邏輯，其他地方則不該有相似邏輯
這裡應該要專門接收 Reward
"""
from zoneinfo import ZoneInfo

from data.event import RewardEvent
from game.model import Player

from cores import event
from cores.logger import logger

taiwan_timezone = ZoneInfo("Asia/Taipei")

class EventRewardHandler:
    @staticmethod
    def provide(event: RewardEvent):
        """
        必定要接收的參數:
        :: user_id
        """
        Player.add_experience(event.payload.user_id, event.payload.experience)
        Player.add_balance(event.payload.user_id, event.payload.currency)

        logger.debug(f"事件 {event.type} 成功推送，獎勵已發放，獎勵: {event.payload.experience} 經驗值, {event.payload.currency} 貨幣")

event.subscribe(RewardEvent, EventRewardHandler.provide)