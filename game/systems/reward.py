from data.event import ActionEvent
from models import Player

from cores import listener

class RewardSystem:
    @staticmethod
    def handle(event: ActionEvent):
        if event.payload.experience is not None:
            Player.add_experience(event.payload.experience)
        
        if event.payload.currency is not None:
            Player.add_balance(event.payload.currency)

listener.subscribe(ActionEvent, RewardSystem.handle)