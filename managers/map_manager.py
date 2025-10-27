from map import Map

class MapManager:
    def __init__(self):
        self._world_map = {
            "forest": Map("forest", "森林"),
            "piedmont": Map("piedmont", "山麓"),
            "river": Map("river", "河畔"),
            "morwel": Map("morwel", "莫威爾")
        }

    @property
    def world_map(self):
        return self._world_map

map_manager = MapManager()