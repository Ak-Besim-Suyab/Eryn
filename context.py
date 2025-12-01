import discord

class Context:

    GUILD_TH_HAVEN = discord.Object(id=1190027756482859038)
    GUILD_AK_BESIM = discord.Object(id=1193049715638538280)

    bot = None
    yaml_loader = None
    state_machine = None

    managers = {}
    handlers = {}
    containers = {}

    skill_entry = {
        "character": "角色", 
        "combat": "戰鬥", 
        "excavation": "採掘"
        }

    @classmethod
    def register_bot(cls, bot):
        cls.bot = bot
        print(f"[Context] Bot registered.")

    @classmethod
    def register_yaml_loader(cls, yaml_loader):
        cls.yaml_loader = yaml_loader
        print(f"[Context] Yaml Loader registered.")

    @classmethod
    def register_state_machine(cls, state_machine):
        cls.state_machine = state_machine
        print(f"[Context] State Machine registered.")

    @classmethod
    def register_manager(cls, name: str, manager: object):
        cls.managers[name] = manager
        print(f"[Context] Manager registered: {name}")

    @classmethod
    def get_manager(cls, name: str):
        return cls.managers.get(name)

    @classmethod
    def register_handler(cls, name: str, handler: object):
        cls.handlers[name] = handler
        print(f"[Context] Handler registered: {name}")

    @classmethod
    def get_handler(cls, name: str):
        return cls.handlers.get(name)

    @classmethod
    def register_container(cls, name: str, container: object):
        cls.containers[name] = container
        print(f"[Context] Container registered: {name}")

    @classmethod
    def get_container(cls, name: str):
        return cls.containers.get(name)

    # in player.py, message_handler.py, data_mamanger.py
    @classmethod
    def get_skill_entry(cls):
        return cls.skill_entry