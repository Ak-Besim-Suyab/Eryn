from state.state import State

from data.command import CommandType
from data.event import EventType

from ui.select import CombatSelect
from ui.views.base_view import BaseView

from context import Context

class CombatState(State):
    def __init__(self, interaction: object):
        self.state = 'combat'
        self.interaction = interaction
        self.player = Context.get_manager("player").get_player(interaction)

    async def start(self, target):
        print(target)
        print(f"{self.interaction.user.display_name}'s combat start")

        action = [{
            "action_id": "attack",
            "action_name": "攻擊",
        }]

        select = CombatSelect(action)
        
        view = BaseView()
        view.add_item(select)

        embed = Embed(CommandType.COMBAT, self.player)
        embed.set_description(target)
        # select attack
        # escape button
        await self.interaction.response.send_message(embed=embed, view=view)

    async def attack(self, target):
        print("attack!")


    async def end(self):
        pass