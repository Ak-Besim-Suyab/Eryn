import discord

from cores import logger
from data import ROLES

async def add(member: discord.Member, role_id: int) -> bool:
    """
    給予成員指定 ID 的 Discord 身分組，返回是否成功
    """
    target = member.guild.get_role(role_id)
    if target is None:
        logger.warning(f"找不到身分組 ID: {role_id}，無法給予 {member.display_name}")
        return False

    if target in member.roles:
        return True

    try:
        await member.add_roles(target, reason="使用下拉式選單套用身分組")
        logger.debug(f"已給予 {member.display_name} 身分組 {target.name} ({role_id})")
        return True
    except discord.Forbidden:
        logger.error(f"沒有權限給予 {member.display_name} 身分組 {target.name} ({role_id})")
        return False
    except discord.HTTPException as e:
        logger.exception(f"給予 {member.display_name} 身分組 {role_id} 時發生錯誤：{e}")
        return False


async def remove(member: discord.Member, role_id: int) -> bool:
    """
    移除成員指定 ID 的 Discord 身分組，返回是否成功
    """
    target = member.guild.get_role(role_id)
    if target is None:
        logger.warning(f"找不到身分組 ID: {role_id}，無法從 {member.display_name} 移除")
        return False

    if target not in member.roles:
        return True

    try:
        await member.remove_roles(target, reason="使用下拉式選單套用身分組時移除同分類身分組")
        logger.debug(f"已移除 {member.display_name} 身分組 {target.name} ({role_id})")
        return True
    except discord.Forbidden:
        logger.error(f"沒有權限移除 {member.display_name} 身分組 {target.name} ({role_id})")
        return False
    except discord.HTTPException as e:
        logger.exception(f"移除 {member.display_name} 身分組 {role_id} 時發生錯誤：{e}")
        return False


async def switch(member: discord.Member, target: int) -> str:
    """
    切換互斥身分組，移除成員身上相同分類的其他身分組，並套用目標身分組，完成後返回結果字串。
    """
    # 取得身分組資料
    role = ROLES.find(id=target)[0]
    if role is None:
        return "❌ 發生錯誤，找不到身分組資料！"

    # 取得身分組物件
    selected_role = member.guild.get_role(role.id)
    if selected_role is None:
        return "❌ 發生錯誤，身分組不存在！"

    try:
        # 取得相同分類的身分組資料
        same_category = ROLES.find(category=role.category) or []
        category_role_ids = {r.id for r in same_category}

        # 取得要移除的其他同類身分組
        removing_roles = [
            r for r in member.roles
            if r.id in category_role_ids and r.id != selected_role.id
        ]

        # 移除其他同類身分組
        if removing_roles:
            await member.remove_roles(
                *removing_roles,
                reason="使用下拉式選單套用身分組時移除同分類身分組",
            )

        # 套用新的身分組
        if selected_role not in member.roles:
            await member.add_roles(
                selected_role,
                reason="使用下拉式選單套用身分組",
            )

        return "✅ 身分組套用成功，在社群頻道裡查看您的外觀吧！"

    except discord.Forbidden:
        logger.error(f"無法套用身分組 {selected_role.name} 給使用者 {member.name}，權限不足")
        return "❌ 發生錯誤，沒有權限套用此身分組！"

    except Exception as e:
        logger.error(f"使用者套用身分組時發生錯誤：{e}")
        return "❌ 套用身分組時發生錯誤，請稍後再試！"
