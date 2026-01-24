import discord

GUILD_TH_HAVEN = discord.Object(id=1190027756482859038)
GUILD_AK_BESIM = discord.Object(id=1193049715638538280)

class Context:

    DUMMY_ID_CYRA = 0
    DUMMY_ID_ERYN = 1
    DUMMY_ID_NYRE = 2

    bot = None
    yaml_loader = None
    json_loader = None

    managers = {}
    
    # 钓鱼系统相关（启动时加载一次）
    fishing_loot_table = None
    items_map = None

    @classmethod
    def register_bot(cls, bot):
        cls.bot = bot

    @classmethod
    def register_yaml_loader(cls, yaml_loader):
        cls.yaml_loader = yaml_loader
    
    @classmethod
    def register_json_loader(cls, json_loader):
        cls.json_loader = json_loader

    @classmethod
    def register_manager(cls, name: str, manager: object):
        cls.managers[name] = manager

    @classmethod
    def get_manager(cls, name: str):
        return cls.managers.get(name)
    
    @classmethod
    def register_fishing_loot_table(cls, loot_table):
        """注册钓鱼掉落表（启动时调用一次）"""
        cls.fishing_loot_table = loot_table