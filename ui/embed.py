import discord

from data.command import CommandType
from data.event import EventType

from formatter import Formatter 
from data.formatter_schema import COMMAND_SCHEMAS, EVENT_SCHEMAS

from context import Context

class LookEmbed(discord.Embed):
    def __init__(self, command_type, player):
        super().__init__(title=player.name, description=self.set_description(command_type, player), color=discord.Color.greyple())

        self.set_image(command_type)

    def set_description(self, command_type, player):
        areas = Context.get_container("area").get_all()

        schema = COMMAND_SCHEMAS[command_type]
        return schema.get("description").format(location=areas.get(player.location).name)

    def set_image(self, command_type):
        schema = COMMAND_SCHEMAS[command_type]
        super().set_image(url=schema.get("image"))

    def add_event_field(self, event_type, data):
        formatter = Formatter(EVENT_SCHEMAS)
        name, value, inline = formatter.format(event_type, data)

        self.add_field(name=name, value=value, inline=inline)