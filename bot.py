import os
import sys
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv

from context import Context
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM

from utils.file_loader import YamlLoader, JsonLoader

# 在導入 registry 之前先初始化 loaders
Context.register_yaml_loader(YamlLoader())
Context.register_json_loader(JsonLoader())

from registry.discord_button_registry import discord_button_manager
from registry.loot_table_registry import loot_table_manager

from managers.item_manager import ItemManager

from database import init_all_databases

from utils.logger import logger

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        init_all_databases()
        
        Context.register_bot(bot)

        Context.register_manager("button", discord_button_manager)
        Context.register_manager("loot_table", loot_table_manager)

        item_manager = ItemManager()

        Context.register_manager("item", item_manager)

        await bot.load_extension("cogs.admin")

        await bot.load_extension("cogs.record")

        await bot.load_extension("cogs.pet")
        await bot.load_extension("cogs.card")
        await bot.load_extension("cogs.leveling")
        await bot.load_extension("cogs.fishing")
        await bot.load_extension("cogs.sell")
        await bot.load_extension("cogs.inventory")
        await bot.load_extension("cogs.shop")
        await bot.load_extension('cogs.role')
        
        await bot.load_extension("cogs.rank")

        await bot.load_extension("cogs.listeners.join")
        await bot.load_extension("cogs.listeners.message")
        await bot.load_extension("cogs.listeners.leveling")

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