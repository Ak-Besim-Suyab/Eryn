from state.state import State

from data.command import CommandType
from data.event import EventType

from context import Context

from ui.view import View
from ui.select import LookSelect
from ui.embed import LookEmbed

class CombatState(State):
    def __init__(self, interaction: object):
        self.state = 'combat'
        self.interaction = interaction

    async def start(self):
        print(f"{self.interaction.user.display_name}'s combat start")
        # select attack
        # escape button

    async def end(self):
        pass