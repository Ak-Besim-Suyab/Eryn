import discord

from data.command import CommandType
from data.event import EventType

from formatter import Formatter 
from data.formatter_schema import EVENT_SCHEMAS

from context import Context

class LookEmbed(discord.Embed):
    def __init__(self, command_type, player):
        super().__init__(title=player.name, description=self.set_description(command_type, player), color=discord.Color.grey())

    def set_description(self, command_type, player):
        areas = Context.get_container("area").get_all()

        description_lines = {
            CommandType.EXCAVATE: "你嘗試在**{location}**某處採掘... 你發現不少東西，並將其放入背包裡",
            CommandType.LOOK: "你查看{location}四周，發現一些目標... 你想選擇誰？"
        }

        return description_lines.get(command_type).format(location=areas[player.location]["name"])

    def set_image(self, command_type):
        image_urls = {
            CommandType.EXCAVATE: "https://cdn.discordapp.com/attachments/1193049715638538283/1430213789252587681/75781c45-a160-4e37-a448-8f49fa3df0bc.png",
            CommandType.LOOK: "https://cdn.discordapp.com/attachments/1193049715638538283/1430214100838781050/75781c45-a160-4e37-a448-8f49fa3df0bc.png"
        }

        super().set_image(url=image_urls[command_type])

    def add_event_field(self, event_type, data):
        formatter = Formatter(EVENT_SCHEMAS)
        name, value, inline = formatter.format(event_type, data)

        self.add_field(name=name, value=value, inline=inline)