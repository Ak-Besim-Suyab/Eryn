import random

from handlers.message_handler import MessageComponent, MessageBuilder

from context import Context

class CaptureHandler:
    def __init__(self):
        self.event_type = "capture"

        print("[CaptureHandler] Handler loaded.")

    async def execute(self, interaction):