import discord
import time
import random

from entity.player_manager import player_manager

from discord.ext import commands
from discord import app_commands

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.social_cooldowns = {}
        self.interval = 5

        print('[Cogs] Social Cog Loaded.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        now = time.time()
        user_id = message.author.id
        self.social_cooldowns.setdefault(user_id, 0)

        if user_id in self.social_cooldowns and now - self.social_cooldowns[user_id] > self.interval:
            player = player_manager.get_player(user_id, message.author.display_name)

            player.skill.social_experience += random.randint(3, 5)
            player.skill.save()
            
            self.social_cooldowns[user_id] = now
        else:
            print("user in cooldown, skip. function here.")
            return

async def setup(bot):
    await bot.add_cog(Social(bot))