import discord
from discord import ui
from discord.ext import commands

from cogs.setting.role_setting import RoleSelect


class FFXIVRoleSettingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ffxiv_role_setting")
    @commands.is_owner()
    async def ffxiv_role_setting(self, ctx: commands.Context):
        await ctx.send(view=FFXIVRoleSettingView())


class FFXIVRoleSettingView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        c = discord.ui.Container(accent_color=0)

        c.add_item(
            discord.ui.TextDisplay(
                "\n".join(
                    [
                        "## <:ffxiv_sprout:1484192636351938621> 最終幻想 XIV 裝飾身分組設定",
                        "> 請注意：同類型的圖案身分組同時只會套用 1 個。",
                    ]
                )
            )
        )
        c.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
        c.add_item(
            ui.ActionRow(
                RoleSelect(
                    placeholder="主題：最終幻想 Final Fantasy",
                    custom_id="select_finalfantasy_role",
                    tag="final_fantasy",
                )
            )
        )

        self.add_item(c)


async def setup(bot: commands.Bot):
    await bot.add_cog(FFXIVRoleSettingCog(bot))
