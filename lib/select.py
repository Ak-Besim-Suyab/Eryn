from discord import ui

from lib import builder

from cores import event_bus
from cores import logger

from data import CONTAINERS
from data.schema.event import SelectEvent

async def post_guide(event: SelectEvent):
    view = ui.LayoutView(timeout = None).add_item(builder.build_container(CONTAINERS.get("post_guide")))
    await event.interaction.response.send_message(view = view, ephemeral = True)

async def select_test(event: SelectEvent):
    await event.interaction.response.send_message("咪，訊息測試成功發送！", ephemeral=True)

def register():
    # 註冊小酒館指南選單
    event_bus.subscribe(SelectEvent, "tavern_guide", post_guide)

    # 註冊測試選單
    event_bus.subscribe(SelectEvent, "select_test", select_test)
    
    logger.info("✅ Select Event Successfully Registered.")