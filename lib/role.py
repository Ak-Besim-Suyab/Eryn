from typing import Iterable

import discord

from cores import logger


async def add(member: discord.Member, role_id: int, reason: str | None = None) -> bool:
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
        await member.add_roles(target, reason=reason)
        logger.debug(f"已給予 {member.display_name} 身分組 {target.name} ({role_id})")
        return True
    except discord.Forbidden:
        logger.error(f"沒有權限給予 {member.display_name} 身分組 {target.name} ({role_id})")
        return False
    except discord.HTTPException as e:
        logger.exception(f"給予 {member.display_name} 身分組 {role_id} 時發生錯誤：{e}")
        return False


async def remove(member: discord.Member, role_id: int, reason: str | None = None) -> bool:
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
        await member.remove_roles(target, reason=reason)
        logger.debug(f"已移除 {member.display_name} 身分組 {target.name} ({role_id})")
        return True
    except discord.Forbidden:
        logger.error(f"沒有權限移除 {member.display_name} 身分組 {target.name} ({role_id})")
        return False
    except discord.HTTPException as e:
        logger.exception(f"移除 {member.display_name} 身分組 {role_id} 時發生錯誤：{e}")
        return False


async def switch(
    member: discord.Member,
    new_role_id: int | None,
    group_role_ids: Iterable[int],
    reason: str | None = None,
) -> bool:
    """
    切換互斥身分組：移除成員身上屬於 group_role_ids 的其他身分組，並套用 new_role_id
    """
    group_id_set = set(group_role_ids)
    removing_roles = [
        r for r in member.roles
        if r.id in group_id_set and r.id != new_role_id
    ]

    try:
        if removing_roles:
            await member.remove_roles(*removing_roles, reason=reason)

        if new_role_id is None:
            return True

        return await add(member, new_role_id, reason=reason)
    except discord.Forbidden:
        logger.error(f"沒有權限切換 {member.display_name} 的身分組 (target={new_role_id})")
        return False
    except discord.HTTPException as e:
        logger.exception(f"切換 {member.display_name} 的身分組時發生錯誤：{e}")
        return False
