from discord import Embed, Interaction

from models.player import Player
from models.region import region_manager
from models.resource import resource_manager



class GardenSkill:
    def __init__(self):
        pass
    
    @classmethod
    async def cast(cls, interaction: Interaction):
        region = region_manager.get_region(Player.get_region(interaction.user.id))

        for res in region.resources:
            resource = resource_manager.get_resource(res)
            record = resource.roll()

            for item_id, amount in record.items():
                # 這裡之後補上邏輯
                print(f"獲得 {amount} 個 {item_id}")

        embed = Embed()
        embed.title = interaction.user.display_name
        embed.description = "採集成功！"

        from interface.action.view import GardenView
        view = GardenView()

        await interaction.followup.send(embed=embed, view=view)