"""
引導至維基頁面的按鈕集，連結按鈕自動持久化，不需要額外處理。
"""

import discord

class MapGuideButton(discord.ui.Button):
    """
    引導至地圖維基
    """
    def __init__(self):

        url = "https://suyab42.notion.site/World-Map-41c66f39eca68088b58af76c598047c4"

        super().__init__(
            style=discord.ButtonStyle.secondary,
            label="查看說明", 
            url=url
        )

class BuildingGuideButton(discord.ui.Button):
    def __init__(self):

        url = "https://suyab42.notion.site/Building-41f66f39eca680f7a65dc7e2eb9b80af"

        super().__init__(
            style=discord.ButtonStyle.secondary,
            label="查看說明", 
            url=url
        )