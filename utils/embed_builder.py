import json
import discord

from context import Context

from utils.logger import logger

class EmbedBuilder:
    def __init__(self):
        self.embed_datas = Context.yaml_loader.load("data/embed_texts.yaml")

    def create(self, key: str, portrait: str = ""):
        embed_list = self.embed_datas.get(key)

        if not embed_list:
            raise ValueError(f"Embed key '{key}' not found in embed_texts")

        if isinstance(embed_list, dict):
            embed_list = [embed_list]

        embeds = []

        # read embeds
        for data in embed_list:
            # ====== read titles ======
            title = data.get("title", None)
            description = data.get("description", None)
            color = data.get("color", 0xFFFFFF)

            embed = discord.Embed(title=title, description=description, color=color)
            logger.info(f'Embed created successfully, name:{key}.')

            # ====== read fields ======
            fields = data.get("field")
            if isinstance(fields, list):
                for f in fields:
                    name = f.get("name", None)
                    value = f.get("value", None)
                    inline = f.get("inline", False)

                    embed.add_field(name=name, value=value, inline=inline)

            # ====== read portrait ======
            p = data.get("portrait", portrait)

            embed.set_thumbnail(url=p)
            logger.info(f'Embed thumbnail set successfully.')

            # ====== store ======
            embeds.append(embed)

        return embeds

# 在其他地方直接導入 embed_builder = EmbedBuilder 
# 輸入關鍵字串建立 embed_builder.create("string", "portrait"可選)