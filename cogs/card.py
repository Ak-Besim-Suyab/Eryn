import discord
from discord import app_commands
from discord.ext import commands

from context import GUILD_TH_HAVEN, GUILD_AK_BESIM

from utils.embed_builder import EmbedBuilder

from database.player import Player

@app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
class CardGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name = "名片", description = "管理你的個人名片")

    # /名片 登記
    # ----------------------------------------------------
    @app_commands.command(name = "登記", description = "登記或更新你的個人名片")
    @app_commands.describe(content = "你想登記的名片內容")
    async def card_register(self, interaction: discord.Interaction, content: str):
        player, _ = Player.get_or_create(id=interaction.user.id)

        if not content:
            return await interaction.response.send_message("登記名片需要填寫內容喔！", ephemeral=True)

        player.card = content
        player.save()

        await interaction.response.send_message("名片已成功更新！", ephemeral=True)

    # /名片 刪除
    # ----------------------------------------------------
    @app_commands.command(name = "刪除", description = "刪除你的個人名片")
    async def card_delete(self, interaction: discord.Interaction):
        player, _ = Player.get_or_create(id=interaction.user.id)

        if not player.card:
            return await interaction.response.send_message("你沒有可以刪除的名片喔！", ephemeral=True)

        player.card = None
        player.save()

        await interaction.response.send_message("你的名片已刪除。", ephemeral=True)

    # /名片 查看
    # ----------------------------------------------------
    @app_commands.command(name = "查看", description = "查看某位使用者的名片")
    @app_commands.describe(target = "你想查看的對象")
    async def card_view(self, interaction: discord.Interaction, target: discord.User):
        target_player, _ = Player.get_or_create(id=target.id)

        card = target_player.card or "這位使用者尚未設定名片。"

        await interaction.response.send_message(
            f"{target.display_name} 的名片：\n```{card}```",
            ephemeral=False
        )

@app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
@app_commands.context_menu(name="查看名片")
async def view_card_user(interaction: discord.Interaction, user: discord.User):
    player, _ = Player.get_or_create(id=user.id)
    card = player.card or "這位使用者尚未設定名片。"

    await interaction.response.send_message(
        f"{user.display_name} 的名片：\n```{card}```",
        ephemeral=True
    )

class Card(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(CardGroup())
        self.bot.tree.add_command(view_card_user)


async def setup(bot):
    await bot.add_cog(Card(bot))