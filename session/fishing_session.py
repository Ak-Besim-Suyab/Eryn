import discord
from datetime import datetime

from engines.fishing_engine import FishingEngine
from ui.views.fishing_view import FishingView

from database.inventory import Inventory
from database.skill import Skill
from database.player import Player

from context import Context

class FishingSession:
    def __init__(self):
        self.engine = FishingEngine()   
        self.view = FishingView(self)
        self.manager = Context.get_manager("item")

        self._fishing_cooldown = 3.5 # seconds
        self._player_cooldown = {}
    
    async def start(self, interaction: discord.Interaction):

        # 取得釣魚技能等級
        player_id = interaction.user.id
        fishing_level = Skill.get_or_create_skill(player_id, "fishing").level

        # 計算玩家冷卻時間
        now = datetime.now()
        fixed_cooldown = max(1.0, self._fishing_cooldown - (fishing_level * 0.02))  # 改用 max 更直觀

        if player_id in self._player_cooldown:
            last_time = self._player_cooldown[player_id]
            elapsed = (now - last_time).total_seconds()
            if elapsed < fixed_cooldown:
                remain_cooldown = fixed_cooldown - elapsed
                await self._post_fishing_not_ready(interaction, remain_cooldown, fixed_cooldown)
                return

        # 更新最後釣魚時間
        self._player_cooldown[player_id] = now

        # 進行釣魚與發送結果
        payload = self.engine.cast()
        if payload:
            await self._post_fish_successed(interaction, payload)
        else:
            await self._post_fish_missed(interaction)
            
    async def _post_fishing_not_ready(self, interaction: discord.Interaction, wait_time: float, cooldown: float):
        content = f"釣魚技能還沒準備好，你還需要等待 {wait_time:.1f} 秒，目前你的釣魚技能冷卻時間為 {cooldown} 秒"
        await interaction.response.send_message(content=content, ephemeral=True)

    async def _post_fish_missed(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=interaction.user.display_name, 
            description="你在附近的水域垂釣，但什麼都沒釣到...", 
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, view=self.view)
    
    async def _post_fish_successed(self, interaction: discord.Interaction, payload):
        player_id = interaction.user.id
        lines = []

        total_experience = 0
        # 解析釣到的物品
        for item in payload:

            # 數據庫更新
            if item.get("event_type") == "general":
                Inventory.add_item(player_id, item['item_id'], item['quantity'])
                total_experience += item['experience']

            elif item.get("event_type") == "treasure":
                player = Player.get_or_create_player(player_id)
                player.add_currency(item['currency'])

            # 紀錄顯示內容
            if "item_id" in item:
                item_obj = self.manager.get_item(item["item_id"])
                item_name = item_obj.get("display_name") if item_obj else item["item_id"]
                lines.append(f"**{item_name}**× {item['quantity']}")

        embed = discord.Embed(
            title = interaction.user.display_name, 
            description = "你在附近的水域垂釣，好像有魚上鉤...", 
            color=discord.Color.blue()
        )

        embed.add_field(
            name="你獲得道具：", 
            value="\n".join(lines), 
            inline=False
        )
        embed.add_field(
            name="你獲得經驗值：", 
            value=f"釣魚 +{sum(item['experience'] for item in payload if 'experience' in item)}", 
            inline=False
        )
        for item in payload:
            if item.get("event_type") == "treasure":
                currency = item.get("currency", 0)
                embed.add_field(
                    name="你在水域附近發現寶藏！",
                    value=f"獲得額外 {currency} 金幣",
                    inline=False
                )
                
        await interaction.response.send_message(embed=embed, view=self.view)

        # leveling check
        level_payload = Skill.add_experience(player_id, "fishing", total_experience)
        if level_payload.get('is_level_up'):
            interaction.client.dispatch("level_up", interaction, "釣魚", level_payload.get('level'))