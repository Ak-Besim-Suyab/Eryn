import discord
from discord.ext import commands
from discord import app_commands

from handler.shop_handler import shop_handler
from player_manager import player_manager

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('[Command] Shop Command Loaded')

    @app_commands.guilds(discord.Object(id=1193049715638538280), discord.Object(id=1190027756482859038))
    @app_commands.command(name="shop", description="購買道具")
    async def shop_menu(self, interaction: discord.Interaction):
        embed = discord.Embed(
                    title=f"{interaction.user.display_name}",
                    description="請選擇想要瀏覽的分類：\n"
                                "牲畜 - 購買能夠放牧的小動物\n"
                                "升級 - 購買各種強化配備", 
                    color=discord.Color.greyple()
                )
        await interaction.response.send_message(embed=embed, view=MainShopView())

class MainShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="動物", style=discord.ButtonStyle.primary)
    async def shop_menu_animals(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = player_manager.get_player(interaction.user.id, interaction.user.display_name)
        await interaction.response.send_message(embed=embed_livestock(interaction, player), view=LivestockView())

    @discord.ui.button(label="裝備", style=discord.ButtonStyle.primary)
    async def shop_menu_equipments(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = player_manager.get_player(interaction.user.id, interaction.user.display_name)
        await interaction.response.send_message(embed=embed_equipments(interaction, player), view=LivestockView())

class LivestockView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        animals = [
            ("chick", "小雞", 4),
            ("lamb", "小羊", 8),
            ("piggy", "小豬", 10)
        ]

        amounts = [1, 5, 10]

        for row, (key, display_name, price) in enumerate(animals):
            for amount in amounts:
                button = discord.ui.Button(
                    label=f"{display_name} ×{amount}",
                    style=discord.ButtonStyle.gray,
                    row=row
                )
                # 使用 lambda 綁定參數
                button.callback = self.make_buy_callback(key, amount)
                self.add_item(button)

    def make_buy_callback(self, item_key: str, amount: int):
        async def callback(interaction: discord.Interaction):
            player = player_manager.get_player(interaction.user.id, interaction.user.display_name)
            shop_handler.buy_item(player, item_key, amount)
            print(f"Purchasing {amount} {item_key}(s)...")
            await interaction.response.edit_message(embed=embed_livestock(interaction, player), view=self)
        return callback

def embed_livestock(interaction, player):
    embed = discord.Embed(
                title=f"{interaction.user.display_name}",
                description=f"🐤 **雛雞** - 4 金幣 你擁有：{player.inventory.item_list.get("chick") or 0}\n"
                            f"*毛茸茸的黃色小球*\n"
                            f"🐑 **羔羊** - 8 金幣 你擁有：{player.inventory.item_list.get("lamb") or 0}\n"
                            f"*別緻的羔羊*\n"
                            f"🐖 **幼豬** - 10 金幣 你擁有：{player.inventory.item_list.get("piggy") or 0}\n"
                            f"*活蹦亂跳的培根*", 
                color=discord.Color.greyple()
            )
    return embed

def embed_equipments(interaction, player):
    embed = discord.Embed(
                title=f"{interaction.user.display_name}",
                description=f"**鐵鎬** - 500 金幣 {"已擁有" if player.inventory.item_list.get("iron_pickaxe") == 1 else "未擁有"}\n"
                            f"*\n"
                            f"**金鎬** - 1000 金幣 {"已擁有" if player.inventory.item_list.get("golden_pickaxe") == 1 else "未擁有"}\n"
                            f"*\n"
                            f"**鑽石鎬** - 10000 金幣 {"已擁有" if player.inventory.item_list.get("diamond_pickaxe") == 1 else "未擁有"}\n", 
                color=discord.Color.greyple()
            )
    return embed

async def setup(bot):
    await bot.add_cog(Shop(bot))