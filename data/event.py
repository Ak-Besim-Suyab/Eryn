from dataclasses import dataclass

from data.type import Type, ActionType
from data.payload import *

@dataclass
class Event:
    type: Type
    payload: Payload = None

@dataclass
class ActionEvent(Event):
    type: ActionType
    payload: ActionPayload = None