import discord
import random
import asyncio
from discord.ext import commands

from ui.selects.cat_select import CatSelectView

from utils.embed_builder import EmbedBuilder

class MemberJoinEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        # ignore discord bot member.
        if member.bot:
            return

        bot_name = self.bot.user.display_name
        bot_image = self.bot.user.display_avatar.url

        view = CatSelectView()

        embed_builder = EmbedBuilder()

        #--------------------------------------------------------
        # direct message part.
        #--------------------------------------------------------

        dialogues = [
            "welcome_message_direct_1",
            "welcome_message_direct_2",
            "welcome_message_direct_3",
            "welcome_message_direct_4"
        ]

        try:
            for dialogue in dialogues:
                embeds = embed_builder.create(
                    dialogue = dialogue, 
                    author = bot_name,
                    portrait = bot_image,
                    timestamp = True
                )
                async with member.typing():
                    await asyncio.sleep(5.0)

                if dialogue in dialogues[-1]:
                    await member.send(embeds=embeds, view=view)
                else:
                    await member.send(embeds=embeds)

        except discord.Forbidden:
            print(f"嘗試私訊新成員 {member} 失敗，新成員可能已關閉私訊設定。")

        #--------------------------------------------------------
        # guild message part.
        #--------------------------------------------------------

        # message pools
        dialogues = [
            "welcome_message_guild_1",
            "welcome_message_guild_2"
        ]

        dialogue = random.choice(dialogues)

        # this message is no author
        embed_to_member = embed_builder.create(
            dialogue = dialogue, 
            portrait = member.display_avatar.url,
            parameters = {
                "member_name": member.display_name
            },
            timestamp = True
        )

        embed_from_eryn = embed_builder.create(
            dialogue = "welcome_message_guild_eryn", 
            author = bot_name,
            portrait = bot_image,
            timestamp = True
        )

        channel = member.guild.system_channel
        if channel:
            await channel.send(embeds=embed_to_member + embed_from_eryn, view=view)

async def setup(bot):
    await bot.add_cog(MemberJoinEvent(bot))