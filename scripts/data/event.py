from dataclasses import dataclass

from scripts.data.type import *
from scripts.data.payloads.response import *

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