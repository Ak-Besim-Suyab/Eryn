from state.state import State

from data.command import CommandType
from data.event import EventType

from context import Context

from ui.views.base_view import BaseView
from ui.views.target_view import TargetView

from ui.select import LookSelect
from ui.embed import EventEmbed

class LookState(State):
    def __init__(self, interaction: object):
        self.state = 'look'
        self.interaction = interaction
        self.player = Context.get_manager("player").get_player(interaction)

    async def start(self):
        areas = Context.get_container("area").get_all()
        
        look_handler = Context.get_handler("look")
        target_entries = look_handler.draw_target(self.player) # [entity.to_dict()]

        area = areas.get(self.player.location)

        content = {
            "area_name": area.name
        }

        select = LookSelect(self, target_entries)

        view = BaseView()
        view.add_item(select)

        embed = EventEmbed(CommandType.LOOK, self.player)
        embed.set_description(content)
        embed.add_event_field(EventType.FIND_ENTITY, target_entries)

        await self.interaction.response.send_message(embed=embed, view=view)

    async def select_entry(self, interaction, entry):

        content = {
            "target_name": entry.get("entity_name")
        }

        embed = EventEmbed(CommandType.TARGET, self.player)
        embed.set_description(content)

        view = TargetView(entry)

        await interaction.response.edit_message(embed=embed, view=view)