# This class is used to manage views registration and creation.
# Views are compiled in ui/views/,
# see the registry at registry/discord_view_registry.py
# -----------------------------------------------------------
# usage：
#     manager = DiscordViewManager()
#     manager.register("my_view", MyView)
#     view = manager.create("my_view")
# -----------------------------------------------------------

class DiscordViewManager: 
    def __init__(self):
        self._registry = {}
    
    # register a view
    def register(self, name: str, view_class):
        if name in self._registry:
            raise ValueError(
                f"View '{name}' 已被註冊，避免重複註冊同一個名稱"
            )
        self._registry[name] = view_class
    
    # create a view
    def create(self, name: str, *args, **kwargs):
        if name not in self._registry:
            available = ", ".join(self.list_views())
            raise ValueError(
                f"View '{name}' 未被註冊。"
                f"可用 View: {available or '(無)'}"
            )
        
        view_class = self._registry[name]
        return view_class(*args, **kwargs)
    
    # check if a view exists
    def exists(self, name: str) -> bool:
        return name in self._registry
    
    # list all registered views
    def list_views(self) -> list:
        return list(self._registry.keys())