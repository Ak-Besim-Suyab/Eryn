import discord
from game import model

class Embed(discord.Embed):
    def __init__(self, embed: model.Embed, **kwargs):

        self.embed = embed

        super().__init__(
            title = embed.title.format(**kwargs) if embed.title else "",
            description = embed.description.format(**kwargs) if embed.description else "",
            color = EMBED_COLOR.get(embed.color, None)
        )

        if embed.image: self.set_image(url=embed.image)
        if embed.thumbnail: self.set_thumbnail(url=embed.thumbnail)
        if embed.author: self.set_author(name=embed.author.name, icon_url=embed.author.icon_url)

        if embed.fields:
            for field in embed.fields:
                self.add_field(
                    name=field.name.format(**kwargs) if field.name else "", 
                    value=field.value.format(**kwargs) if field.value else "", 
                    inline=field.inline
                )

EMBED_COLOR = {
    "gold"        : discord.Color.gold(),
    "dark_gold"   : discord.Color.dark_gold(),
    "orange"      : discord.Color.orange(),
    "dark_orange" : discord.Color.dark_orange(),
    "light_grey"  : discord.Color.light_grey(),
    "dark_grey"   : discord.Color.dark_grey(),
    "dark_theme"  : discord.Color.dark_theme(),
}