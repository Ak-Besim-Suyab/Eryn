import discord
import os
import json
from discord.ext import commands
from pathlib import Path

from game.model import Player

from cores.logger import logger

class AdminMemberCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --------------------------------------------------------
    # Profile Command Group ----------------------------------
    # --------------------------------------------------------
    @commands.group()
    @commands.is_owner()
    async def profile(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            logger.info("使用 !profile + 子指令呼叫對應方法")


    @profile.command(name="create_all")
    @commands.is_owner()
    async def create_all(self, ctx: commands.Context):
        folder_path = "assets/members"
        guild = ctx.guild

        if not os.path.exists(folder_path):
            logger.error("資料夾不存在或存在錯誤，請檢查資料夾路徑是否正確。")
            return

        for member in guild.members:
            profile_path = f"{folder_path}/{member.id}.json"

            if os.path.exists(profile_path):
                logger.info(f"成員 {member.display_name} 的檔案已存在。")
                continue
            
            # 初始資料
            data = {
                "user_id": member.name,
                "user_name": member.display_name,
                "house": []
            }

            # 這裡是只建立檔案，不進行任何寫入，因此參數設置為 "x"
            with open(profile_path, "x", encoding='utf-8') as file:
                json.dump(
                    data, 
                    file, 
                    indent=4, 
                    ensure_ascii=False
                )
                logger.info(f"成員 {member.display_name} 的檔案尚未存在，已建立新檔。")


    @profile.command(name="refresh_all")
    @commands.is_owner()
    async def refresh_all(self, ctx: commands.Context):
        folder_path = "assets/members"
        guild = ctx.guild

        if not os.path.exists(folder_path):
            logger.error("資料夾不存在或存在錯誤，無法更新資料，請檢查資料夾路徑是否正確。")
            return
        
        profile_unestablished = []
        
        for member in guild.members:
            profile_path = f"{folder_path}/{member.id}.json"

            if not os.path.exists(profile_path):
                profile_unestablished.append(member.display_name)
                logger.info(f"成員 {member.display_name} 的檔案不存在，無法更新。")
                continue

            with open(profile_path, "r", encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    logger.error(f"成員 {member.display_name} 的檔案格式錯誤，導致無法更新。")
                    continue

            # 要更新的資料項目
            # user_id
            if data["user_id"]:
                logger.info(f"成員 {member.display_name} 的舊 ID 為 {data['user_id']}，現在覆蓋為 {member.name}。")
            else:
                logger.info(f"成員 {member.display_name} 的舊 ID 為空，現在覆蓋為 {member.name}。")
            data["user_id"] = member.name

            # user_name
            if data["user_name"]:
                logger.info(f"成員 {member.display_name} 的舊名稱為 {data['user_name']}，現在覆蓋為 {member.display_name}。")
            else:
                logger.info(f"成員 {member.display_name} 的舊名稱為空，現在覆蓋為 {member.display_name}。")
            data["user_name"] = member.display_name

            # 寫入
            with open(profile_path, "w", encoding='utf-8') as file:
                json.dump(
                    data, 
                    file, 
                    indent=4, 
                    ensure_ascii=False
                )
                logger.info(f"成員 {member.display_name} 的檔案更新成功。")

            for member in profile_unestablished:
                logger.info(f"成員 {member} 的檔案不存在，無法更新。")

    @profile.command(name="check_all")
    @commands.is_owner()
    async def check_all(self, ctx: commands.Context):
        """反查成員狀態：找出已退出和新成員"""
        folder_path = "assets/members"
        guild = ctx.guild
        
        if not os.path.exists(folder_path):
            logger.error("資料夾不存在，無法進行反查。")
            return
        
        # 獲取所有檔案中的成員 ID
        file_member_ids = set()
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                member_id = filename.replace(".json", "")
                file_member_ids.add(member_id)
        
        # 獲取所有 guild 成員的 ID
        guild_member_ids = {str(member.id) for member in guild.members}
        
        # 找出已退出的成員（在檔案中但不在 guild.members）
        departed_members = file_member_ids - guild_member_ids
        logger.info(f"已退出的成員數量：{len(departed_members)}")
        for member_id in sorted(departed_members):
            profile_path = f"{folder_path}/{member_id}.json"
            try:
                with open(profile_path, "r", encoding='utf-8') as file:
                    data = json.load(file)
                    user_name = data.get("user_name", "未知")
                    logger.info(f"  [已退出] {user_name} (ID: {member_id})")
            except (json.JSONDecodeError, FileNotFoundError):
                logger.info(f"  [已退出] ID: {member_id}")
        
        # 找出新成員（在 guild.members 但沒有檔案）
        new_members = guild_member_ids - file_member_ids
        logger.info(f"新成員數量：{len(new_members)}")
        for member_id in sorted(new_members):
            member = guild.get_member(int(member_id))
            if member:
                logger.info(f"  [新成員] {member.display_name} (ID: {member_id})")
    # --------------------------------------------------------
    # --------------------------------------------------------

    @commands.command()
    @commands.is_owner()
    async def all_rank(self, ctx: commands.Context):
        tops = Player.select().order_by(
            Player.level.desc(), 
            Player.experience.desc()
        )

        total = 0
        for _, player in enumerate(tops, start=1):
            member = ctx.guild.get_member(player.id)
            if member:
                total += 1
                logger.info(f"{member.display_name} 等級 {player.level} / {player.experience} Exp")
            else:
                logger.info(f"未找到成員 - {player.display_name} | ID - {player.id} 可能已離開群組。")

        logger.info(f"有排名的成員總數為：{total} 人")
                

async def setup(bot):
    await bot.add_cog(AdminMemberCog(bot))