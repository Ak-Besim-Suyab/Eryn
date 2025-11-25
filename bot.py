import discord
from discord.ext import commands

from context import Context
from state.state_machine import StateMachine

from loot_loader import LootLoader

from managers.player_manager import PlayerManager
from managers.data_manager import DataManager

from handlers.excavate_handler import ExcavateHandler
from handlers.look_handler import LookHandler

from models.item import ItemContainer
from models.area import AreaContainer
from models.entity import EntityContainer

from state.look_state import LookState
from state.combat_state import CombatState

import traceback
import sys
import os

from dotenv import load_dotenv

from utils.logger import logger

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        #await bot.load_extension("cogs.home")
        #await bot.load_extension("cogs.world")
        await bot.load_extension("cogs.look")
        await bot.load_extension("cogs.announcement")
        await bot.load_extension("cogs.server_info")
        #await bot.load_extension("cogs.play")
        #await bot.load_extension("cogs.hello")
        #await bot.load_extension("cogs.excavate")

        synced_haven = await bot.tree.sync(guild=Context.GUILD_TH_HAVEN)
        synced_besim = await bot.tree.sync(guild=Context.GUILD_AK_BESIM)

        Context.register_bot(bot)
        Context.register_loader(LootLoader())
        Context.register_state_machine(StateMachine())

        Context.register_manager("player", PlayerManager())
        Context.register_manager("data", DataManager())

        Context.register_handler("excavate", ExcavateHandler())
        Context.register_handler("look", LookHandler())

        Context.register_container("item", ItemContainer())
        Context.register_container("area", AreaContainer())
        Context.register_container("entity", EntityContainer())

        Context.state_machine.register("look", LookState)
        Context.state_machine.register("combat", CombatState)

        Context.get_manager("data").load_database()

        Context.get_container("item").register()
        Context.get_container("area").register()
        Context.get_container("entity").register()

        logger.info(f'Synced {len(synced_haven)} commands to guild Ak Besim')
        logger.info(f'Synced {len(synced_besim)} commands to guild Th Haven')
        logger.info(f'The version of python is {sys.version}')
        logger.info(f'Discord Bot loaded, Enjoy!')
        
    except Exception as e:
        logger.error(f'Error syncing commands:{e}')
        traceback.print_exc() 
        
    logger.info(f"✅ 已登入：{bot.user}")
    
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot.run(TOKEN)