import os
import sys
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv

from context import Context
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM
from state.state_machine import StateMachine

from file_loader import YamlLoader

from handlers.excavate_handler import ExcavateHandler
from handlers.look_handler import LookHandler

from models.item import ItemContainer
from models.area import AreaContainer
from models.entity import EntityContainer

from state.look_state import LookState
from state.combat_state import CombatState

from registry.button_registry import button_manager

from database.dummy import init_dummy_database
from database.player import init_player_database

from utils.logger import logger

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        init_dummy_database()
        init_player_database()

        await bot.load_extension("cogs.member_join_event")

        await bot.load_extension("cogs.test_embed")

        await bot.load_extension("cogs.pet")
        await bot.load_extension("cogs.card")

        synced_haven = await bot.tree.sync(guild=GUILD_TH_HAVEN)
        synced_besim = await bot.tree.sync(guild=GUILD_AK_BESIM)

        Context.register_bot(bot)
        Context.register_yaml_loader(YamlLoader())
        # Context.register_state_machine(StateMachine())

        Context.register_manager("button", button_manager)

        # Context.register_handler("excavate", ExcavateHandler())
        # Context.register_handler("look", LookHandler())

        # Context.register_container("item", ItemContainer())
        # Context.register_container("area", AreaContainer())
        # Context.register_container("entity", EntityContainer())

        # Context.state_machine.register("look", LookState)
        # Context.state_machine.register("combat", CombatState)

        # Context.get_container("item").register()
        # Context.get_container("area").register()
        # Context.get_container("entity").register()

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