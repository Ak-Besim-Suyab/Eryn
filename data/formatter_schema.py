from data.event import EventType
from data.command import CommandType

EVENT_SCHEMAS = {
    EventType.LEVEL_UP: {
        "expected_keys": {
            "skill_id": str,
            "old_level": int,
            "new_level": int
        },
        "line_template": "{skill_name}等級 Lv.{old_level} → Lv.{new_level}",
        "field_name": "升級！",
        "inline": False,
    },
    EventType.OBTAIN_ITEM: {
        "expected_keys": {
            "image": str,
            "name": str,
            "quantity": int
        },
        "line_template": "{image} {name} x{quantity}",
        "field_name": "獲得物品：",
        "inline": False,
    },
    EventType.OBTAIN_EXPERIENCE: {
        "expected_keys": {
            "skill_id": str,
            "experience": int
        },
        "line_template": "{skill} +{experience} EXP",
        "field_name": "獲得經驗：",
        "inline": False,
    },
    EventType.FIND_ENTITY: {
        "expected_keys": {
            "entity_name": str,
            "level": int,
            "image": str
        },
        "line_template": "{image} {entity_name} Lv.{level}",
        "field_name": "附近有：",
        "inline": False,
    }
}

COMMAND_SCHEMAS = {
    CommandType.LOOK: {
        "image": "https://cdn.discordapp.com/attachments/1193049715638538283/1430214100838781050/75781c45-a160-4e37-a448-8f49fa3df0bc.png",
        "description": "你查看**{area_name}**四周，發現一些目標... 你想選擇誰？"
    },
    CommandType.TARGET: {
        "image": "https://cdn.discordapp.com/attachments/1193049715638538283/1430214100838781050/75781c45-a160-4e37-a448-8f49fa3df0bc.png",
        "description": "你選擇**{name}**做為目標，接下來要做什麼？"
    },
    CommandType.EXCAVATE: {
        "image": "https://cdn.discordapp.com/attachments/1193049715638538283/1430214100838781050/75781c45-a160-4e37-a448-8f49fa3df0bc.png",
        "description": "你嘗試在**{area_name}**某處採掘... 你發現不少東西，並將其放入背包裡"
    },
    CommandType.COMBAT: {
        "image": "https://cdn.discordapp.com/attachments/1193049715638538283/1430214100838781050/75781c45-a160-4e37-a448-8f49fa3df0bc.png",
        "description": "要對**{name}**採取什麼攻擊？"
    }
}