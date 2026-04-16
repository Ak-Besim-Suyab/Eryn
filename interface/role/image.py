import discord

image_college_of_arms = "https://cdn.discordapp.com/attachments/1193049715638538283/1483857918532128808/college_of_arms_img.png"

class RoleImage(discord.Embed):
    def __init__(self):
        super().__init__()
        self.color = discord.Color.gold()
        self.set_image(url=image_college_of_arms)