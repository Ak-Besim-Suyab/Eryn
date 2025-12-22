import json
import discord

from context import Context

from utils.logger import logger

DIALOGUE_PATH = "data/dialogues.yaml"

# --------------------------------------------------
# this is a utility for creating embed message.
# --------------------------------------------------
class EmbedBuilder:
    def __init__(self):
        self.embed_datas = Context.yaml_loader.load(DIALOGUE_PATH)

    def create(self, 
            dialogue: str, 
            author: str = "",
            portrait: str = "", 
            color = 0xFFFFFF,
            parameters: dict = None,
            timestamp = False
        ):

        # protect default mutable argument problem.
        if parameters is None:
            parameters = {}

        embed_list = self.embed_datas.get(dialogue)
        if not embed_list:
            raise ValueError(f"Dialogue name '{dialogue}' not found in {DIALOGUE_PATH}")

        if isinstance(embed_list, dict):
            embed_list = [embed_list]

        # formatting tool.
        formatted = lambda string: string.format(**parameters) if isinstance(string, str) else string

        embeds = []

        # read embeds
        for data in embed_list:
            #--- set title ------------------------------------------
            title = data.get("title")
            description = data.get("description")
            color = data.get("color", color)

            embed = discord.Embed(
                title=formatted(title), 
                description=formatted(description), 
                color=color)

            #--- set fields -----------------------------------------
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

            #--- set author -----------------------------------------
            embed.set_author(
                name = data.get("author", author),
                icon_url = data.get("portrait", portrait)
            )

            #--- set thumbnail --------------------------------------
            embed.set_thumbnail(
                url=data.get("portrait", portrait)
            )

            #--- show time stamp ------------------------------------
            if timestamp:
                embed.timestamp = discord.utils.utcnow()

            #--- store embed ----------------------------------------
            embeds.append(embed)


        logger.info(f'Embed created successfully: {dialogue}.')
        return embeds

# 在其他地方直接導入 embed_builder = EmbedBuilder 
# 輸入關鍵字串建立 embed_builder.create("string", author=, portrait=, )