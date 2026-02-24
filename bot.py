import os
import sys
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv

from context import Context
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM

from cores.loader import YamlLoader, JsonLoader

# 在導入 registry 之前先初始化 loaders
Context.register_yaml_loader(YamlLoader())
Context.register_json_loader(JsonLoader())

from database import init_all_databases

from cores.logger import logger

from ui.views.daily_reward import DailyRewardView

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class Elin(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.add_view(DailyRewardView(self))


bot = Elin()


@bot.event
async def on_ready():
    try:
        init_all_databases()
        
        Context.register_bot(bot)

        await bot.load_extension("cogs.admin")
        await bot.load_extension("cogs.daily")
        await bot.load_extension("cogs.leveling")
        await bot.load_extension("cogs.role")
        await bot.load_extension("cogs.stat")

        await bot.load_extension("cogs.listeners.join")
        await bot.load_extension("cogs.listeners.leveling")
        await bot.load_extension("cogs.listeners.message")

        synced_haven = await bot.tree.sync(guild=GUILD_TH_HAVEN)
        synced_besim = await bot.tree.sync(guild=GUILD_AK_BESIM)

        logger.info(f'Synced {len(synced_haven)} commands to guild Th Haven')
        logger.info(f'Synced {len(synced_besim)} commands to guild Ak Besim')

        logger.info(f'The version of python is {sys.version}')
        logger.info('Discord Bot loaded, Enjoy!')
        
    except Exception as e:
        logger.error(f'Error syncing commands:{e}')
        traceback.print_exc() 
        
    logger.info(f"✅ 已登入：{bot.user}")
    
def main():
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)

if __name__ == "__main__":
    main()