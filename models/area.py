from context import Context

class Area:
    def __init__(self, ID: str, name: str):
        self.ID = ID
        self.name = name

        print(f"[Log|Area] {self.ID} registered.")

class AreaContainer:
    def __init__(self):
        self.areas: dict[str, Area] = {}

    def register(self):
        data_areas = Context.loader.load("data/areas")

        for ID, data in data_areas.items():
            self.areas[ID] = Area(ID=ID, name=data.get("name"))

    def get_area(self, map_id: str):
        return self.areas[map_id]

    def get_area_all(self):
        return self.areas