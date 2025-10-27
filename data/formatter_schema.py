from data.event import EventType

EVENT_SCHEMAS = {
    EventType.LEVEL_UP: {
        "expected_keys": {
            "skill_name": str,
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
        "field_name": "獲得物品",
        "inline": False,
    },
    EventType.OBTAIN_EXPERIENCE: {
        "expected_keys": {
            "skill": str,
            "experience": int
        },
        "line_template": "{skill} +{experience} EXP",
        "field_name": "獲得經驗",
        "inline": False,
    },
    EventType.FIND_ENTITY: {
        "expected_keys": {
            "image": str,
            "name": str,
            "level": int
        },
        "line_template": "{image} {name} Lv.{level}",
        "field_name": "附近有",
        "inline": False,
    }
}