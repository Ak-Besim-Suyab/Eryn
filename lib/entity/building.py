from peewee import fn

from cores.database import database
from cores.logger import logger

from data.enums import MaterialName

from models import Building
from models import Contribution

from lib import material

def get(building_id: str) -> Building:
    building, _ = Building.get_or_create(id=building_id)
    return building

def add_contribution(
        player_id: int, 
        building_id: str, 
        resource_id: str, 
        quantity: int) -> tuple[bool, str]:
    
    """
    增加建築的資源貢獻同時移除玩家資源, 返回是否成功與訊息
    """

    # 確保貢獻與建築物資料存在
    Building.get_or_create(id=building_id)
    Contribution.get_or_create(building=building_id, player=player_id)

    with database.atomic():

        # 移除玩家材料, 參數合法性, 材料數量都交由材料模組處理, 這裡只負責接收是否成功
        success, msg = material.remove(player_id, resource_id, quantity)

        if not success:
            return False, msg

        # 增加建築物貢獻值, 需要查詢兩個外鍵, 否則會變成增加所有建築物或所有玩家指定欄位上的值
        (Contribution
            .update(**{resource_id: getattr(Contribution, resource_id) + quantity})
            .where(Contribution.building == building_id)
            .where(Contribution.player   == player_id)
            .execute())

    logger.debug(f"成功給予 {player_id} {quantity} 個 {resource_id} 到 {building_id}")
    return True, "成功"

def get_contribution(building_id: str, res: str) -> int:
    """
    取得單位指定資源貢獻值總和，返回字典：資源名稱為 key, 總數為 value
    """

    if not material.is_valid(res):
        raise ValueError

    column = getattr(Contribution, res)

    contribution = (Contribution
                    .select(fn.COALESCE(fn.SUM(column), 0))
                    .where(Contribution.building == building_id)
                    .scalar())

    return contribution

def get_contributions(building_id: str) -> dict[str, int]:
    """
    取得建築的所有資源貢獻值總和, 返回資源名稱為鍵, 總數為值的字典
    """
    sum = [
        fn.COALESCE(fn.SUM(getattr(Contribution, mat)), 0).alias(mat)
        for mat in MaterialName]

    rows = (Contribution
            .select(*sum)
            .where(Contribution.building == building_id)
            .dicts()
            .get())

    return rows

def add_experience(building_id: str, amount: float):

    if amount < 0:
        raise ValueError

    updated = (Building
               .update(experience = Building.experience + amount)
               .where(Building.id == building_id)
               .execute())

    if updated:
        upgrade(building_id)

        logger.info(f"已為 {building_id} 增加 {amount} 點經驗值")

def get_experience(building_id: str) -> float:
    return round(Building.select(Building.experience).where(Building.id == building_id).scalar(), 1)

def get_experience_requirement(level: int, 
                               base: int = 1000, 
                               exponent: float = 1.225, 
                               addition: int = 50) -> float:
    """
    返回單位升級所需要的`experience`經驗值
    """
    
    return round(base * (level ** exponent) + level * addition, 1)

def get_reqrsc(level: int, 
               base: int = 1350, 
               exponent: float = 1.15) -> float:
    """
    返回單位資源升級所需的`contrubution`貢獻值總量
    """
    
    return round((base * level ** exponent) / 10) * 10

def get_rlevel(build_id: str, resource: str) -> int:
    current = get_contribution(build_id, resource)
    level = 1
    
    while True:
        required = get_reqrsc(level)
        if current >= required:
            level += 1
        else:
            break

    return level

def get_level(building_id: str) -> int:
    return Building.select(Building.level).where(Building.id == building_id).scalar()
        
def upgrade(building_id: str) -> tuple[bool, int]:
    """ 
    升級建築，返回`upgraded: bool`表示升級與否和`level: int`表示當前等級
    """
    upgrade = False
    with database.atomic():
        while True:

            # 每個循環重新獲取資料庫，避免其他來源的變更或本次更新後造成未同步問題
            building: Building
            building, _ = Building.get_or_create(id=building_id)

            # 每個循環重新獲取升級所需經驗
            require = get_experience_requirement(building.level)
            current = get_experience(building_id)

            # 檢查是否滿級或經驗值是否符合升級條件
            if require is None or current < require:
                break

            # 更新建築物等級
            updated = (Building
                .update(level=Building.level + 1)
                .where(Building.id == building_id)
                .where(Building.level == building.level)
                .execute()
            )

            # 檢查是否成功更新, 避免競讀發生
            if not updated:
                break

            upgrade = True

            logger.info(f"單位 {building_id} 升級成功，現在等級為 {building.level}")

    return upgrade, building.level