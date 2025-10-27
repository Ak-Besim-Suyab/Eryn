import discord

from ui.embed import Embed

from context import Context

class MessageComponent:
    def __init__(self, event_type):
        self.event_type = event_type
        self.events = []

    def add(self, type: str, data: any):
        self.events.append({ "type": type, "data": data })

    def get_all(self):
        return self.events

class MessageBuilder:
    def __init__(self, component: MessageComponent):
        self.component = component

    def build(self, player):
        # init embed message with selected event type
        areas = Context.get_container("area_container").get_area_all()

        skills = Context.get_skill_entry()

        embed = Embed()
        embed.title = player.name
        embed.description = self.get_description(self.component.event_type).format(location=areas[player.location].name)
        embed.color = discord.Color.greyple()

        embed.set_image(url=self.get_image(self.component.event_type))
        #embed.set_thumbnail(url=self.get_thumbnail(self.event_type))

        for event in self.component.get_all():
            type = event["type"]
            data = event["data"]

            if type == "excavation_result":

                lines = [f"{items[name].image} {items[name].name} x{quantity}" for name, quantity in data.items()]
                message = "\n".join(lines)
                embed.add_field(name="獲得物品：", value=message or "（沒有任何獎勵）", inline=True)

            elif type == "exp_gain":

                lines = [f"{skills.get(name)} +{quantity} EXP" for name, quantity in data.items()]
                message = "\n".join(lines)
                embed.add_field(name="獲得經驗：", value=message, inline=True)

            elif type == "additional_event":

                lines = [f"{additional_item} x{quantity}" for additional_item, quantity in data.items()]
                message = "\n".join(lines)
                embed.add_field(name="你挖到某個冒險者的遺體...", value=message, inline=False)

            elif type == "choose":

                embed.add_field(name="", value="你打算選擇誰為目標？", inline=False)

        return embed

    async def send(self, interaction, player):

        if self.component.event_type == "excavation":
            cog = "Excavate"
        elif self.component.event_type == "look":
            cog = "Look"
        else:
            cog = "unknown"

        view = Context.bot.get_cog(cog).get_view()

        await interaction.response.send_message(embed=self.build(player), view=view)

    def get_thumbnail(self, event):
        thumbnails = {
            "excavation": "https://cdn.discordapp.com/attachments/1193049715638538283/1427761990176079985/pickaxe_1.png",
            "taming": "https://cdn.discordapp.com/attachments/1193049715638538283/1427761990176079985/pickaxe_1.png"
        }
        return thumbnails.get(event)