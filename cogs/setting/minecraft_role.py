from discord.ext import commands

from ui.views import RoleSettingView

TITLE = "<:minecraft_pufferfish:1484222619439071363> 麥塊身分組（圖案）"
MEDIA = "https://cdn.discordapp.com/attachments/1491046495812718672/1574574777333457027/minecraft_sift_1.png"
TAG   = "minecraft"


class MinecraftRoleSettingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="minecraft_role_setting")
    @commands.is_owner()
    async def minecraft_role_setting(self, ctx: commands.Context):
        await ctx.send(view=RoleSettingView(title=TITLE, media=MEDIA, tag=TAG))


async def setup(bot: commands.Bot):
    await bot.add_cog(MinecraftRoleSettingCog(bot))
    bot.add_view(RoleSettingView(title=TITLE, media=MEDIA, tag=TAG))
