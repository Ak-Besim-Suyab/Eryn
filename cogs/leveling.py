import discord
from discord.ext import commands, tasks
from datetime import datetime
from database.character import Character
from database.skill import Skill
from utils.logger import logger

BROADCAST_CHANNEL_ID = 1450110904912969800

MESSAGE_EXP = 5  # 每條消息獲得的經驗值
MESSAGE_COOLDOWN = 30  # 冷卻時間（秒），防止洗頻

VOICE_EXP_PER_MINUTE = 1  # 語音每分鐘獲得的經驗值

class Leveling(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.message_cooldowns = {}  # {user_id: last_timestamp}
        self.voice_task_first_run = True  # 標記是否為第一次執行
        self.voice_exp_task.start()
    
    def cog_unload(self):
        """當 Cog 被卸載時停止定時任務"""
        self.voice_exp_task.cancel()
    
    # ========================
    # 訊息事件 - 獲得經驗值
    # ========================
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 跳過 bot 訊息
        if message.author.bot:
            return
        
        # 跳過私訊
        if not message.guild:
            return
        
        user_id = message.author.id
        now = datetime.now().timestamp()
        
        # 檢查冷卻時間
        if user_id in self.message_cooldowns:
            if now - self.message_cooldowns[user_id] < MESSAGE_COOLDOWN:
                return
        
        # 更新冷卻時間戳
        self.message_cooldowns[user_id] = now
        
        try:
            # 增加經驗值
            result = Character.add_experience(user_id, MESSAGE_EXP)
            
            # 如果升級了，發送升級通知
            if result['leveled_up']:
                await self._send_level_up_notification(
                    message.guild,
                    message.author,
                    "character",
                    result['new_levels']
                )
                logger.info(f"[升級] {message.author} 在 character 系統升級到 Lv.{result['level']}")
            
        except Exception as e:
            logger.error(f"[錯誤] 處理訊息經驗時出錯：{e}")
    
    # ========================
    # 語音事件 - 每分鐘自動結算
    # ========================
    
    @tasks.loop(minutes=1)
    async def voice_exp_task(self):
        """每分鐘自動結算一次語音經驗"""
        
        # 第一次執行時跳過（避免機器人啟動時立即結算）
        if self.voice_task_first_run:
            self.voice_task_first_run = False
            logger.info("[語音] 語音經驗定時任務已啟動，跳過第一次結算")
            return
        
        try:
            for guild in self.bot.guilds:
                for voice_channel in guild.voice_channels:
                    for member in voice_channel.members:
                        if member.bot:
                            continue
                        
                        result = Character.add_experience(member.id, VOICE_EXP_PER_MINUTE)
                        
                        logger.debug(f"[語音] {member} 在 {voice_channel.name} 獲得 {VOICE_EXP_PER_MINUTE} 經驗")
                        
                        if result['leveled_up']:
                            await self._send_level_up_notification(
                                guild,
                                member,
                                "character",
                                result['new_levels']
                            )
                            logger.info(f"[升級] {member} 在 character 系統升級到 Lv.{result['level']}")
        
        except Exception as e:
            logger.error(f"[錯誤] 語音經驗定時任務出錯：{e}")
    
    @voice_exp_task.before_loop
    async def before_voice_exp_task(self):
        await self.bot.wait_until_ready()
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        if member.bot:
            return
        
        if after.channel and not before.channel:
            logger.info(f"[語音] {member} 加入語音頻道：{after.channel.name}")
        
        elif before.channel and not after.channel:
            logger.info(f"[語音] {member} 離開語音頻道：{before.channel.name}")
    
    # ========================
    # 升級通知 - 廣播頻道
    # ========================
    
    async def _send_level_up_notification(self, guild: discord.Guild, user: discord.User, system_type: str, new_levels: list):
        """
        在廣播頻道發送升級通知
        
        參數：
            guild：伺服器對象
            user：玩家對象
            system_type：系統類型（"character", "fishing", "mining" 等）
            new_levels：升級到的等級列表（例如 [11, 12]）
        
        流程：
        1. 獲取廣播頻道
        2. 檢查是否可以發送訊息
        3. 構建並發送升級訊息
        """
        
        try:
            # 獲取廣播頻道
            broadcast_channel = guild.get_channel(BROADCAST_CHANNEL_ID)
            
            # 檢查頻道是否存在
            if not broadcast_channel:
                logger.warning(f"[警告] 找不到廣播頻道 ID: {BROADCAST_CHANNEL_ID}")
                return
            
            # 檢查機器人是否有發送訊息權限
            if not broadcast_channel.permissions_for(guild.me).send_messages:
                logger.warning(f"[警告] 機器人沒有在廣播頻道 {broadcast_channel.name} 的發送訊息權限")
                return
            
            # 系統類型的中文名稱
            system_names = {
                "character": "角色",
                "fishing": "釣魚",
                "mining": "挖礦"
            }
            system_name = system_names.get(system_type, system_type)
            
            # 構建升級訊息
            if len(new_levels) == 1:
                # 升級一級
                level_text = f"升級到 **Lv.{new_levels[0]}**"
            else:
                # 升級多級
                level_text = f"升級到 **Lv.{new_levels[-1]}** (一次升級 {len(new_levels)} 級！)"
            
            embed = discord.Embed(
                title="🎉 玩家升級",
                description=f"{user.mention} 的{system_name}等級 {level_text}",
                color=discord.Color.gold()
            )
            embed.set_thumbnail(url=user.display_avatar.url)
            
            # 發送訊息
            await broadcast_channel.send(embed=embed)
            
        except Exception as e:
            logger.error(f"[錯誤] 發送升級通知時出錯：{e}")
    
    # ========================
    # 管理員指令
    # ========================
    
    @commands.command(name="等級管理")
    @commands.has_permissions(administrator=True)
    async def level_admin_command(self, ctx, member: discord.Member, action: str, value: int):
        """
        管理員指令：管理玩家的等級和經驗值
        
        用法：
            !等級管理 @玩家 設置等級 <等級>    - 設置玩家的等級（經驗重設為 0）
            !等級管理 @玩家 設置經驗 <經驗值>  - 設置玩家的經驗值
            !等級管理 @玩家 增加經驗 <經驗值>  - 增加玩家的經驗值
            !等級管理 @玩家 重設等級             - 將玩家重設為 Lv.1，經驗 0
        
        例子：
            !等級管理 @某玩家 設置等級 10       - 將該玩家設為 Lv.10
            !等級管理 @某玩家 設置經驗 500     - 將該玩家的經驗設為 500
            !等級管理 @某玩家 增加經驗 100     - 給該玩家增加 100 經驗
            !等級管理 @某玩家 重設等級          - 將該玩家重設為初始狀態
        """
        try:
            # 只允許 bot 管理員（guild owner 或有管理員權限的人）
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("❌ 你沒有權限執行此指令（需要管理員權限）")
                return
            
            player_id = member.id
            
            # 設置等級
            if action == "設置等級":
                if value < 1:
                    await ctx.send("❌ 等級必須 >= 1")
                    return
                
                result = Character.set_level(player_id, value)
                embed = discord.Embed(
                    title="⚙️ 等級已設置",
                    description=f"玩家：{member.mention}\n原等級：Lv.{result['old_level']}\n新等級：Lv.{result['level']}\n經驗值：重設為 0",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
                logger.info(f"[管理] {ctx.author} 將 {member} 的等級從 Lv.{result['old_level']} 設為 Lv.{result['level']}")
            
            # 設置經驗
            elif action == "設置經驗":
                if value < 0:
                    await ctx.send("❌ 經驗值必須 >= 0")
                    return
                
                result = Character.set_experience(player_id, value)
                progress = Character.get_progress(player_id)
                embed = discord.Embed(
                    title="⚙️ 經驗值已設置",
                    description=f"玩家：{member.mention}\n當前等級：Lv.{result['level']}\n原經驗值：{result['old_experience']}\n新經驗值：{result['experience']}/{progress['required_exp']}",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
                logger.info(f"[管理] {ctx.author} 將 {member} 的經驗值從 {result['old_experience']} 設為 {result['experience']}")
            
            # 增加經驗
            elif action == "增加經驗":
                if value <= 0:
                    await ctx.send("❌ 增加的經驗值必須 > 0")
                    return
                
                result = Character.add_experience(player_id, value)
                embed = discord.Embed(
                    title="➕ 經驗已增加",
                    description=f"玩家：{member.mention}\n增加經驗：{value}\n當前等級：Lv.{result['level']}\n當前經驗值：{result['experience']}",
                    color=discord.Color.green()
                )
                
                # 如果升級了，在 embed 中顯示
                if result['leveled_up']:
                    embed.add_field(
                        name="🎉 升級",
                        value=f"升級到 Lv.{result['level']} (升級等級：{result['new_levels']})",
                        inline=False
                    )
                    
                    # 發送升級通知到廣播頻道
                    await self._send_level_up_notification(
                        ctx.guild,
                        member,
                        "character",
                        result['new_levels']
                    )
                
                await ctx.send(embed=embed)
                logger.info(f"[管理] {ctx.author} 給 {member} 增加了 {value} 經驗，當前 Lv.{result['level']}")
            
            # 重設等級
            elif action == "重設等級":
                result = Character.set_level(player_id, 1)
                embed = discord.Embed(
                    title="🔄 等級已重設",
                    description=f"玩家：{member.mention}\n原等級：Lv.{result['old_level']}\n新等級：Lv.1\n經驗值：0/120",
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
                logger.info(f"[管理] {ctx.author} 將 {member} 的等級重設（從 Lv.{result['old_level']} 到 Lv.1）")
            
            else:
                await ctx.send(f"❌ 未知的操作：{action}\n\n支持的操作：設置等級、設置經驗、增加經驗、重設等級")
        
        except ValueError as e:
            await ctx.send(f"❌ 參數錯誤：{e}")
        except Exception as e:
            await ctx.send(f"❌ 操作失敗：{e}")
            logger.error(f"[錯誤] 管理員指令執行失敗：{e}")
    
    @level_admin_command.error
    async def level_admin_error(self, ctx, error):
        """處理管理員指令的錯誤"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ 你沒有權限執行此指令（需要管理員權限）")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "❌ 參數不完整\n\n"
                "用法：\n"
                "  !等級管理 @玩家 設置等級 <等級>\n"
                "  !等級管理 @玩家 設置經驗 <經驗值>\n"
                "  !等級管理 @玩家 增加經驗 <經驗值>\n"
                "  !等級管理 @玩家 重設等級"
            )
        else:
            logger.error(f"[錯誤] 管理員指令錯誤：{error}")


async def setup(bot):
    """註冊 Leveling Cog"""
    await bot.add_cog(Leveling(bot))
