# This class is used to manage buttons registration and creation.
# Buttons are compiled in ui/buttons/,
# see the registry at registry/button_registry.py
# -----------------------------------------------------------
# usage：
#     manager = DiscordButtonManager()
#     manager.register("my_button", MyButton)
#     button = manager.create("my_button")
# -----------------------------------------------------------

class DiscordButtonManager: 
    def __init__(self):
        self._registry = {}
    
    # register a button
    def register(self, name: str, button_class):
        if name in self._registry:
            raise ValueError(
                f"按鈕 '{name}' 已被註冊，避免重複註冊同一個名稱"
            )
        self._registry[name] = button_class
    
    # create a button
    def create(self, name: str, *args, **kwargs):
        if name not in self._registry:
            available = ", ".join(self.list_buttons())
            raise ValueError(
                f"按鈕 '{name}' 未被註冊。"
                f"可用按鈕：{available or '(無)'}"
            )
        
        button_class = self._registry[name]
        return button_class(*args, **kwargs)
    
    # check if a button exists
    def exists(self, name: str) -> bool:
        return name in self._registry
    
    # list all registered buttons
    def list_buttons(self) -> list:
        return list(self._registry.keys())