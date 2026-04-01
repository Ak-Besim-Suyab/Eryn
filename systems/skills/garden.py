from models.player import Player
from models.region import region_manager
from models.resource import resource_manager

class GardenSkill:
    def __init__(self):
        pass
    
    @classmethod
    def cast(cls, user_id: int) -> dict[str, int]:
        region = region_manager.get_region(Player.get_region(user_id))

        result = {}
        for res in region.resources:
            resource = resource_manager.get_resource(res)
            record = resource.roll()
            result.update(record)

            for item_id, amount in record.items():
                # 這裡之後補上邏輯
                print(f"獲得 {amount} 個 {item_id}")

        return result