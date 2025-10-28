from state.state import State

from data.command import CommandType
from data.event import EventType

from context import Context

from ui.view import View
from ui.select import LookSelect
from ui.embed import LookEmbed

class LookState(State):
    def __init__(self, interaction: object):
        self.interaction = interaction

    async def start(self):
        player_manager = Context.get_manager("player")
        player = player_manager.get_player(self.interaction)

        areas = Context.get_container("area").get_all()
        
        look_handler = Context.get_handler("look")
        found_entity = look_handler.draw_entity(player)

        area = areas.get(player.location)

        content = {
            "area_name": area.name
        }

        select = LookSelect(self, found_entity)

        view = View()
        view.add_item(select)

        embed = LookEmbed(player, CommandType.LOOK)
        embed.set_description(content)
        embed.add_event_field(EventType.FIND_ENTITY, found_entity)

        await self.interaction.response.send_message(embed=embed, view=view)

    async def on_target(self, target):
        print(e)
        # embed 選擇 target 做為目標，接下來要做什麼？
        # button 對話 攻擊 捕獲 返回
        pass

    async def end(self):
        pass