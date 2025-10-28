from context import Context

class Area:
    def __init__(self, uid: str, name: str):
        self.uid = uid
        self.name = name

        print(f"[Log|Area] UID:{self.uid} registered.")

class AreaContainer:
    def __init__(self):
        self.areas: dict[str, Area] = {}

    def register(self):
        data_areas = Context.loader.load("data/areas")

        for uid, data in data_areas.items():
            self.areas[uid] = Area(uid=uid, name=data.get("name"))

    def get_area(self, uid: str):
        return self.areas[uid]

    def get_all(self):
        return self.areas