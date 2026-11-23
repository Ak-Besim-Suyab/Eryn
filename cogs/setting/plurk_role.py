from discord.ext import commands

from ui.views import RoleSettingView

TITLE = "<:fox_1_baby_1:1267438830546583585> 噗浪 Plurk 身分組（圖案）"
MEDIA = "https://cdn.discordapp.com/attachments/1491046495812718672/1574496239456882840/ffxiv_evercold.png"
POOL  = "plurk"


class PlurkRoleSettingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="plurk_role_setting")
    @commands.is_owner()
    async def plurk_role_setting(self, ctx: commands.Context):
        await ctx.send(view=RoleSettingView(title=TITLE, media=MEDIA, pool=POOL))


async def setup(bot: commands.Bot):
    await bot.add_cog(PlurkRoleSettingCog(bot))
    bot.add_view(RoleSettingView(title=TITLE, media=MEDIA, pool=POOL))
