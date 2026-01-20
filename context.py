import discord

GUILD_TH_HAVEN = discord.Object(id=1190027756482859038)
GUILD_AK_BESIM = discord.Object(id=1193049715638538280)

class Context:

    DUMMY_ID_CYRA = 0
    DUMMY_ID_ERYN = 1
    DUMMY_ID_NYRE = 2

    bot = None
    yaml_loader = None

    managers = {}

    @classmethod
    def register_bot(cls, bot):
        cls.bot = bot

    @classmethod
    def register_yaml_loader(cls, yaml_loader):
        cls.yaml_loader = yaml_loader

    @classmethod
    def register_manager(cls, name: str, manager: object):
        cls.managers[name] = manager

    @classmethod
    def get_manager(cls, name: str):
        return cls.managers.get(name)