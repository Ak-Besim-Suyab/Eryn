import random
from cores import Action
from utils import cooldown

from cores import event_bus
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

        event_bus.publish(event)

        return event
