import discord

from data.command import CommandType
from data.event import EventType

from formatter import Formatter 
from data.formatter_schema import COMMAND_SCHEMAS, EVENT_SCHEMAS

from context import Context

class EventEmbed(discord.Embed):
    def __init__(self, command_type, player):
        self.command_type = command_type
        self.player = player
        self.set_image()

        super().__init__(title=player.name, description="", color=discord.Color.greyple())

    def set_image(self):
        schema = COMMAND_SCHEMAS[self.command_type]
        super().set_image(url=schema.get("image"))

    def set_description(self, context):
        schema = COMMAND_SCHEMAS[self.command_type]
        self.description = schema.get("description").format(**context)

    def add_event_field(self, event_type, data):
        formatter = Formatter(EVENT_SCHEMAS)
        name, value, inline = formatter.format(event_type, data)

        self.add_field(name=name, value=value, inline=inline)