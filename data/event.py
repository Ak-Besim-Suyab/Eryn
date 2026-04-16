from dataclasses import dataclass

from data.type import *
from data.payload import *

@dataclass
class Event:
    type: Type
    payload: Payload = None

@dataclass
class ActionEvent(Event):
    type: ActionType
    payload: ActionPayload = None

@dataclass
class RewardEvent(Event):
    type: RewardType
    payload: RewardPayload = None