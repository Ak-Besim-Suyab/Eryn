from discord import ui
from lib import builder
import data
from data.schema.event import SelectEvent

async def post_guide(event: SelectEvent):
    view = ui.LayoutView(timeout = None).add_item(builder.build_container(data.container.get("post_guide")))
    await event.interaction.response.send_message(view = view, ephemeral = True)