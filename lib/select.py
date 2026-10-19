import discord

from cores import event_bus
from cores import logger

from schema.event import SelectEvent

from data.registry import role_data

async def select_unique_role(event: SelectEvent):

    if event.custom_id != "select_unique_role":
        return

    # 取得身分組資料
    data = role_data.get(event.value[0])

    # 取得伺服器對應身分組
    selected_role = event.interaction.guild.get_role(data.discord_id)
    if selected_role is None:
        await event.interaction.response.send_message("❌ 發生錯誤，該身分組不存在，請聯絡管理員", ephemeral=True)
        return

    # 嘗試套用身分組
    try:
        # 取得所有身分組資料
        all_data = role_data.get_all()

        # 移除所有同分類的身分組，確保只有一個相同分類的身分組被套用
        for role in event.interaction.user.roles:
            for d in all_data:
                # 判斷使用者的身分組是否在身分組註冊表中，是的話，判斷該身分組 (使用 all_role) 是否與選擇的身分組同分類
                if d.discord_id == role.id and d.category == data.category:
                        await event.interaction.user.remove_roles(role)

        await event.interaction.user.add_roles(role, reason="使用下拉式選單套用身分組")
        
        await event.interaction.response.send_message("✅ 身分組套用成功，在社群頻道裡查看您的外觀吧！", ephemeral=True)
    except discord.errors.Forbidden:
        await event.interaction.response.send_message("❌ 出現預期外的錯誤，咪沒有權限套用該身分組... 請管理員檢查權限！", ephemeral=True)
    except Exception as e:
        await event.interaction.response.send_message("❌ 出現預期外的錯誤，請管理員檢查！", ephemeral=True)
        logger.exception(f"使用者套用身分組時發生錯誤：{e}")

async def select_test(event: SelectEvent):

    if event.custom_id != "select_test":
        return
    
    await event.interaction.response.send_message("咪，訊息測試成功發送！", ephemeral=True)

event_bus.subscribe(SelectEvent, select_unique_role)
event_bus.subscribe(SelectEvent, select_test)