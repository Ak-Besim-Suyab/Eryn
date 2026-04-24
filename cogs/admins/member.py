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
        folder_path = "data/members"
        guild = ctx.guild

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

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
        folder_path = "data/members"
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