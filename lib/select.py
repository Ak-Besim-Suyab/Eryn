import discord

from cores import event_bus
from cores import logger

from schema.event import SelectEvent

from data.registry import role_data

async def select_unique_role(event: SelectEvent):

    await event.interaction.response.defer()

    # 取得身分組資料
    data = role_data.get(event.values[0])

    # 取得伺服器對應身分組
    selected_role = event.interaction.guild.get_role(data.discord_id)
    if selected_role is None:
        await event.interaction.followup.send("❌ 發生錯誤，該身分組似乎不存在，請回報管理員！", ephemeral=True)
        return

    # 嘗試套用身分組
    try:
        # 取得相同分類的身分組資料, 用於檢查唯一身分組
        category_roles = role_data.find(category = data.category)
        category_roles_ids = [role.discord_id for role in category_roles]

        # 取得要移除的其他同類身分組
        removing_roles = [role for role in event.interaction.user.roles if role.id in category_roles_ids]

        # 移除其他同類身分組, 接著套用新的身分組
        await event.interaction.user.remove_roles(*removing_roles, reason="套用唯一身分組，移除其他相同分類身分組")
        await event.interaction.user.add_roles(selected_role, reason="使用下拉式選單套用身分組")
        
        await event.interaction.followup.send("✅ 身分組套用成功，在社群頻道裡查看您的外觀吧！", ephemeral=True)
    except discord.errors.Forbidden:
        await event.interaction.followup.send("❌ 出現預期外的錯誤，咪沒有權限套用該身分組... 請管理員檢查權限！", ephemeral=True)
    except Exception as e:
        await event.interaction.followup.send("❌ 出現預期外的錯誤，請管理員檢查日誌！", ephemeral=True)
        logger.exception(f"使用者套用身分組時發生錯誤：{e}")

async def select_test(event: SelectEvent):
    await event.interaction.response.send_message("咪，訊息測試成功發送！", ephemeral=True)

def register():
    
    event_bus.subscribe(SelectEvent, "select_minecraft_role", select_unique_role)
    event_bus.subscribe(SelectEvent, "select_finalfantasy_role", select_unique_role)
    event_bus.subscribe(SelectEvent, "select_pikmin_role", select_unique_role)
    event_bus.subscribe(SelectEvent, "select_afternoon_tea_role", select_unique_role)
    event_bus.subscribe(SelectEvent, "select_plurk_role", select_unique_role)

    event_bus.subscribe(SelectEvent, "select_flower_role", select_unique_role)
    event_bus.subscribe(SelectEvent, "select_food_role", select_unique_role)
    event_bus.subscribe(SelectEvent, "select_gradient_role", select_unique_role)

    event_bus.subscribe(SelectEvent, "select_test", select_test)
    
    logger.info("✅ Select Event Registered.")