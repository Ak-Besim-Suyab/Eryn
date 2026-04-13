import random
from cores import Action
from utils import cooldown

from cores import listener
from data import *

class MournAction(Action):
    def __init__(self):
        super().__init__()

    @cooldown(seconds = 1.9)
    async def execute(self):
        event = ActionEvent(type = ActionType.STEALING)

        experience = random.randint(1, 9)
        currency = random.randint(1, 9)

        payload = ActionPayload(experience = experience, currency = currency)
        payload.message = Message(title = "mourn_success")
        event.payload = payload

        listener.publish(event)

        # logger.info(f"{interaction.user.display_name} 在緬懷活動中總共獲得 {experience + bonus_experience} 經驗值")

        return event
