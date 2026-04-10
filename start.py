import os, sys, traceback

from dotenv import load_dotenv

from config import TH_HAVEN

from bot import Elin
from cores.logger import logger

bot = Elin()

@bot.event
async def on_ready():
    try:
        # 啟動時先歷遍成員是否在頻道內，如果在頻道內就存儲當前時間戳
        guild = bot.get_guild(TH_HAVEN)
        from systems.level_session import LevelSession
        level_session = LevelSession(bot)
        for member in guild.members:
            if member.voice and member.voice.channel:
                if member.bot:
                    continue
                level_session.save_timestamp(member)

        logger.info(f'The Version of Python is {sys.version}')
        logger.info(f'Meow, Discord Bot loaded!')
        
    except Exception as e:
        logger.error(f'Error syncing commands: {e}')
        traceback.print_exc() 
        
    logger.info(f"✅ Logged in as: {bot.user}")
    
def main():
    load_dotenv()
    token = os.getenv("discord_token")
    bot.run(token)

if __name__ == "__main__":
    main()