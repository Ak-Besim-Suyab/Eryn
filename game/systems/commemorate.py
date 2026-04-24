import discord
import random
from cores import Action
from utils import cooldown

from cores import event
from data import *

class CommemorateAction(Action):
    def __init__(self):
        super().__init__()

    @cooldown(seconds = 2.0)
    async def execute(self, interaction: discord.Interaction):

        user_id = interaction.user.id

        experience = random.randint(1, 9)
        currency = random.randint(1, 9)

        reward_payload = RewardPayload(user_id=user_id)
        reward_payload.experience = experience
        reward_payload.currency = currency

        reward_event = RewardEvent(type=RewardType.LOOT, payload=reward_payload)
        await event.publish(reward_event)

        payloads = {
            "experience": experience,
            "currency": currency
        }

_instance = CommemorateAction()
execute = _instance.execute