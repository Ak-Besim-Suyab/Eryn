from state.state import State

from data.command import CommandType
from data.event import EventType

from context import Context

from ui.view import View
from ui.select import LookSelect
from ui.embed import LookEmbed

class LookState(State):
    def __init__(self, interaction: object):
        self.state = 'look'
        self.interaction = interaction
        self.player = Context.get_manager("player").get_player(interaction)

    async def start(self):
        areas = Context.get_container("area").get_all()
        
        look_handler = Context.get_handler("look")
        target_entries = look_handler.draw_target(self.player)

        area = areas.get(self.player.location)

        content = {
            "area_name": area.name
        }

        select = LookSelect(self, target_entries)

        view = View()
        view.add_item(select)

        embed = LookEmbed(self.player, CommandType.LOOK)
        embed.set_description(content)
        embed.add_event_field(EventType.FIND_ENTITY, target_entries)

        await self.interaction.response.send_message(embed=embed, view=view)

    async def select_entry(self, interaction, entry):

        content = {
            "target_name": entry.get("entity_name")
        }

        embed = LookEmbed(self.player, CommandType.TARGET)
        embed.set_description(content)

        commands = [CommandType.COMBAT, CommandType.HOME]

        view = TargetView(entry)
        for command in commands:
            view.add_item(Context.get_container("button").get_button(command))

        await interaction.response.edit_message(embed=embed, view=view)

    async def end(self):
        pass