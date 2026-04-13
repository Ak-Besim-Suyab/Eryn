import discord
import random
from cores import Action
from utils import cooldown

from cores import listener
from data import *

class StealAction(Action):

    def __init__(self):
        super().__init__()

    @cooldown(seconds = 3.0)
    async def execute(self, interaction: discord.Interaction, member: discord.Member):
        """
        技能邏輯：
        發動成功時，產生獎勵（經驗值、通貨與其他）
        """
        event = ActionEvent(type = ActionType.STEALING)

        if random.random() < 0.35:
            await interaction.response.send_message("偷竊失敗！")
            return

        if member.bot:
            await interaction.response.send_message("喵喵喵！咪沒有東西可以偷！")
            return

        if interaction.user.id == member.id:
            await interaction.response.send_message("你不能偷自己的物品！")
            return

        experience = random.randint(1, 5)
        currency = random.randint(1, 5)

        payload = ActionPayload(
            message = Message(title = "stealing_success"),
            sender_name = interaction.user.display_name,
            target_name = member.display_name,
            experience = experience, 
            currency = currency
        )
        event.payload = payload

        listener.publish(event)

        return event
