from discord.ext import commands
import json
from models.item import Item

class ItemManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.items: dict[str, Item] = {} # item data will be stored as {name: object}
        self.register_item()
        print("[ItemManagerClass] ItemManager loaded.")

    def register_item(self):
        loader = Context.loader
        mudstone = Item(ID="mudstone", name="泥岩", image=loader.load("a"))
        slate = Item(ID="slate", name="板岩")
        metal_ore = Item(ID="metal_ore", name="金屬碎塊")
        antique_silver_coin = Item(ID="antique_silver_coin", name="舊銀幣")

        self.items["mudstone"] = mudstone
        self.items["slate"] = slate
        self.items["metal_ore"] = metal_ore
        self.items["antique_silver_coin"] = antique_silver_coin

        self.load_image("mudstone")
        self.load_image("slate")
        self.load_image("metal_ore")
        self.load_image("antique_silver_coin")

    def load_image(self, ID: str):
        path = f"textures/{ID}.json"
        try: 
            with open(path, "r", encoding="utf-8") as f:
                image = json.load(f)["image"]
                self.items[ID].image = image
        except Exception as e:
            print(f"[ImageLoader] load texture {ID} failed, use default texture.")
            print(e)

    def get(self, ID: str) -> Item | None:
        return self.items.get(ID)

async def setup(bot):
    await bot.add_cog(ItemManager(bot))