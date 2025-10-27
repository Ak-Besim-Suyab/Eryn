import discord
from discord.ext import commands
from discord import app_commands

from context import Context

GUILD_TH_HAVEN = discord.Object(id=1193049715638538280)
GUILD_AK_BESIM = discord.Object(id=1190027756482859038)

class Home(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.view = HomeView()
        print('[Cogs] Home Cog Loaded.')

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="home", description="打開 ERYN 主頁，包含指令與遊戲畫面")
    async def home(self, interaction: discord.Interaction):
        await self.open_menu(interaction)

    async def open_menu(self, interaction: discord.Interaction):
        embed = discord.Embed(
                    title=f"{interaction.user.display_name}",
                    description="歡迎你回到家，溫暖且舒適的地方",
                    color=discord.Color.greyple()
                )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1193049715638538283/1430743510864236564/inv_1.png")
        embed.add_field(name="目前：", value="雖然這裡什麼都還沒有，但我相信很快會有的", inline=False)
        embed.add_field(name="行動地點：", value="**森林**", inline=False)
        embed.set_footer(text="Eryn 的悄悄話：行動時會前往行動地點")
        embed_e = discord.Embed(
                    title=f"悄悄話",
                    description="採掘獲得的材料可以加工成製品，然後賣個好價錢",
                    color=discord.Color.greyple()
                )
        embed_e.set_image(url="https://cdn.discordapp.com/attachments/1193049715638538283/1430743510864236564/inv_1.png")
        await interaction.response.send_message(embeds=[embed, embed_e], view=self.view)

    def get_view(self):
        return self.view

class HomeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.button_stat = discord.ui.Button(label="狀態", style=discord.ButtonStyle.primary)
        self.button_inventory = discord.ui.Button(label="背包", style=discord.ButtonStyle.primary)
        self.button_action = discord.ui.Button(label="行動", style=discord.ButtonStyle.primary)
        self.button_map = discord.ui.Button(label="地圖", style=discord.ButtonStyle.primary)
        self.button_shop = discord.ui.Button(label="商店", style=discord.ButtonStyle.secondary)
        self.button_info = discord.ui.Button(label="關於 Eryn", style=discord.ButtonStyle.secondary)

        self.button_stat.callback = self.no_action
        self.button_inventory.callback = self.no_action
        self.button_action.callback = self.no_action
        self.button_map.callback = self.location
        self.button_shop.callback = self.no_action
        self.button_info.callback = self.callback_info

        self.add_item(self.button_stat)
        self.add_item(self.button_inventory)
        self.add_item(self.button_action)
        self.add_item(self.button_map)
        self.add_item(self.button_shop)
        self.add_item(self.button_info)

    async def no_action(self, interaction: discord.Interaction):
        await interaction.response.send_message("未實裝，請期待！")

    async def callback_info(self, interaction: discord.Interaction):
        embed = discord.Embed(
                    title=f"關於艾琳（Eryn）",
                    description="艾琳是以其內建同名文字遊戲為主體的遊戲兼功能性機器人\n"
                                "透過與 Discord 原生功能強相關的遊戲設計，來豐富遊戲與伺服器的頻道生態",
                    color=discord.Color.greyple()
                )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1193049715638538283/1430743510864236564/inv_1.png")
        embed.set_footer(text="悄悄話：艾琳也有許多實用的指令")
        await interaction.response.send_message(embed=embed, view=self)

    async def location(self, interaction: discord.Interaction):
        embed = discord.Embed(
                    title=f"關於艾琳（Eryn）",
                    description="艾琳是以內置的同名文字遊戲為主的 Discord Bot\n"
                                "透過與 Discord 原生功能強相關的遊戲設計，來豐富伺服器的文字頻道生態",
                    color=discord.Color.greyple()
                )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1193049715638538283/1430743510864236564/inv_1.png")
        embed.set_footer(text="悄悄話：艾琳也有許多實用的指令")
        await interaction.response.send_message(embed=embed, view=self)


async def setup(bot):
    await bot.add_cog(Home(bot))