from state.state import State

from data.command import CommandType
from data.event import EventType

from context import Context

from ui.view import View
from ui.select import LookSelect
from ui.embed import LookEmbed

class ExcavateState(State):
    def __init__(self, interaction: object):
        player_manager = Context.get_manager("player")
        self.player = player_manager.get_player(interaction)
        self.interaction = interaction

    async def start(self):
        excavate_handler = Context.get_handler("excavate")
        excavate_result = excavate_handler.draw(self.player)
        experience_result = excavate_handler.draw_experience()

        for entry in excavate_result:
            self.player.inventory.add_item(entry["item_id"], entry["quantity"])

        for entry in experience_result:
            skill = getattr(self.player.skill, entry["skill_id"])
            skill.experience += entry["experience"]

        embed = LookEmbed(CommandType.EXCAVATE, self.player)
        embed.set_image(CommandType.EXCAVATE)
        embed.add_event_field(EventType.OBTAIN_ITEM, excavate_result)
        embed.add_event_field(EventType.OBTAIN_EXPERIENCE, experience_result)

        leveling_result = self.player.skill.process_all_leveling()
        if leveling_result:
            embed.add_event_field(EventType.LEVEL_UP, leveling_result)

        await self.interaction.response.send_message(embed=embed)
        await self.end()

    async def end(self):
        self.player.update()