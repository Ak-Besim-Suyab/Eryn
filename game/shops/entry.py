import discord
from views import MarketView

class ShopKeeper:
    @staticmethod
    async def open(shop_name: str, interaction: discord.Interaction):
        descriptions = [
            "> 這裡是海岸旁最喧囂的港口集市。",
            "> 商品、攤販與人群盡收眼底，香料與海洋的味道飄散著。",
            "> 有價值的事物可能就在某個不被照耀的角落。",
        ]
        
        embed = discord.Embed()
        embed.title = "市集"
        embed.description = "\n".join(descriptions)
        embed.color = discord.Color.gold()

        embed.add_field(name="", value="要做什麼？", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1491046495812718672/1491046587244351528/market.png")

        view = MarketView()
        
        await interaction.response.send_message(embed=embed, view=view)