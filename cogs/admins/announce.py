from discord.ext import commands
from discord import ui

from data import container_data
from lib import builder

"""
此元件用於管理所有公告訊息
"""

class AnnounceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def announce(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("請使用 !announce + 子指令呼叫方法", ephemeral=True)

    # 測試項目 -------------------------------------

    @announce.command(name="template")
    @commands.is_owner()
    async def template(self, ctx: commands.Context):
        view = ui.LayoutView(timeout = None).add_item(builder.build_container(container_data.get("template")))
        await ctx.send(view = view)

    @announce.command(name="template_param")
    @commands.is_owner()
    async def template_param(self, ctx: commands.Context):
        
        param = {
            "name": "Elin",
            "level": 1,
            "experience": 100
        }

        view = ui.LayoutView(timeout = None).add_item(builder.build_container(container_data.get("template_param"), **param))
        await ctx.send(view = view)

    # ---------------------------------------------

    @announce.command(name="travel_guide")
    @commands.is_owner()
    async def travel_guide(self, ctx: commands.Context):
        view = ui.LayoutView(timeout = None).add_item(builder.build_container(container_data.get("travel_guide")))
        await ctx.send(view = view)

    @announce.command(name="explore_guide")
    @commands.is_owner()
    async def explore_guide(self, ctx: commands.Context):
        view = ui.LayoutView(timeout = None).add_item(builder.build_container(container_data.get("explore_guide")))
        await ctx.send(view = view)

    @announce.command(name="channel_guide")
    @commands.is_owner()
    async def channel_guide(self, ctx: commands.Context):
        view = ui.LayoutView(timeout = None).add_item(builder.build_container(container_data.get("channel_guide")))
        await ctx.send(view = view)

    @announce.command(name="cabin_guide")
    @commands.is_owner()
    async def cabin_guide(self, ctx: commands.Context):
        view = ui.LayoutView(timeout = None).add_item(builder.build_container(container_data.get("cabin_guide")))
        await ctx.send(view = view)

    @announce.command(name="community_rule")
    @commands.is_owner()
    async def community_rule(self, ctx: commands.Context):
        view = ui.LayoutView(timeout = None).add_item(builder.build_container(container_data.get("community_rule")))
        await ctx.send(view = view)

    @announce.command(name="role_book")
    @commands.is_owner()
    async def role_book(self, ctx: commands.Context):
        view = ui.LayoutView(timeout = None).add_item(builder.build_container(container_data.get("role_book")))
        await ctx.send(view = view)

    @announce.command(name="attendance")
    @commands.is_owner()
    async def attendance(self, ctx: commands.Context):
        view = ui.LayoutView(timeout = None).add_item(builder.build_container(container_data.get("attendance")))
        await ctx.send(view = view)

async def setup(bot: commands.Bot):
    await bot.add_cog(AnnounceCog(bot))