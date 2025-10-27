from state.state import State

from data.command import CommandType
from data.event import EventType

from context import Context

from ui.view import View
from ui.select import Select
from ui.embed import LookEmbed

class LookState(State):
    def __init__(self, interaction: object):
        self.interaction = interaction

    async def start(self):
        player_manager = Context.get_manager("player")
        player = player_manager.get_player(self.interaction)
        
        look_handler = Context.get_handler("look")
        found_entity = look_handler.draw_entity()

        select = LookSelect(found_entity)

        view = View()
        view.add_item(select)

        embed = LookEmbed(CommandType.LOOK, player)
        embed.add_event_field(EventType.FIND_ENTITY, found_entity)

        await self.interaction.response.send_message(embed=embed, view=view)

    async def end(self):
        pass