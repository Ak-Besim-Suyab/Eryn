import discord
from discord.ext import commands

from context import Context

from loot_loader import LootLoader

from managers.player_manager import PlayerManager
from managers.data_manager import DataManager

from handlers.excavation_handler import ExcavationHandler
from handlers.look_handler import LookHandler

from models.item import ItemContainer
from models.area import AreaContainer
from models.entity import EntityContainer

import traceback
import sys
import os

from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        await bot.load_extension("cogs.home")
        await bot.load_extension("cogs.world")
        await bot.load_extension("cogs.look")
        await bot.load_extension("cogs.play")
        await bot.load_extension("cogs.hello")
        await bot.load_extension("cogs.excavate")

        synced_haven = await bot.tree.sync(guild=Context.GUILD_TH_HAVEN)
        synced_besim = await bot.tree.sync(guild=Context.GUILD_AK_BESIM)

        Context.register_bot(bot)
        Context.register_loader(LootLoader())
        Context.register_manager("player", PlayerManager())
        Context.register_manager("data", DataManager())

        Context.register_handler("excavate", ExcavationHandler())
        Context.register_handler("look", LookHandler())

        Context.register_container("item", ItemContainer())
        Context.register_container("area", AreaContainer())
        Context.register_container("entity", EntityContainer())

        Context.get_manager("data").load_database()

        Context.get_container("item").register()
        Context.get_container("area").register()
        Context.get_container("entity").register()

        print(f'Synced {len(synced_haven)} commands to guild Ak Besim')
        print(f'Synced {len(synced_besim)} commands to guild Th Haven')
        print(f'The version of python is {sys.version}')

        print(f'Discord Bot loaded, Enjoy!')
    except Exception as e:
        print(f'Error syncing commands:{e}')
        traceback.print_exc() 
        
    print(f"✅ 已登入：{bot.user}")
    
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot.run(TOKEN)