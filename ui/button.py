import discord

CHARACTER_BUTTON = discord.ui.Button(style=discord.ButtonStyle.secondary, label="查看角色卡", custom_id="character_tab")
RESOURCE_BUTTON = discord.ui.Button(style=discord.ButtonStyle.secondary, label="查看資源", custom_id="resource_tab")

MAP_GUIDE_BUTTON = discord.ui.Button(
    style=discord.ButtonStyle.secondary, 
    label="查看地圖說明",
    url="https://suyab42.notion.site/World-Map-41c66f39eca68088b58af76c598047c4")

BUILDING_GUIDE_BUTTON = discord.ui.Button(
    style=discord.ButtonStyle.secondary, 
    label="查看說明",
    url="https://suyab42.notion.site/Building-41f66f39eca680f7a65dc7e2eb9b80af")