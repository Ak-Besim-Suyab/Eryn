import json
import discord

from context import Context

from utils.logger import logger

class EmbedBuilder:
    def __init__(self):
        self.embed_datas = Context.yaml_loader.load("data/embed_texts.yaml")

    def create(self, 
            key: str, 
            author: str = "",
            portrait: str = "", 
            parameters: dict = None
        ):

        # protect default mutable argument problem.
        if parameters is None:
            parameters = {}

        embed_list = self.embed_datas.get(key)
        if not embed_list:
            raise ValueError(f"Embed key '{key}' not found in embed_texts")

        if isinstance(embed_list, dict):
            embed_list = [embed_list]

        # formatting tool.
        formatted = lambda string: string.format(**parameters) if isinstance(string, str) else string

        embeds = []

        # read embeds
        for data in embed_list:
            # ====== read titles ======
            title = data.get("title")
            description = data.get("description")
            color = data.get("color", 0xFFFFFF)

            embed = discord.Embed(
                title=formatted(title), 
                description=formatted(description), 
                color=color)

            # ====== read fields ======
            fields = data.get("field")
            if isinstance(fields, list):
                for f in fields:
                    name = f.get("name")
                    value = f.get("value")
                    inline = f.get("inline", False)

                    embed.add_field(
                        name=formatted(name), 
                        value=formatted(value), 
                        inline=inline)

            # set author
            embed.set_author(
                name = data.get("author", author),
                icon_url = data.get("portrait", portrait)
            )

            # set thumbnail
            embed.set_thumbnail(
                url=data.get("portrait", portrait)
            )

            # store embed
            embeds.append(embed)

        logger.info(f'Embed created successfully: {key}.')
        return embeds

# 在其他地方直接導入 embed_builder = EmbedBuilder 
# 輸入關鍵字串建立 embed_builder.create("string", author=, portrait=, )