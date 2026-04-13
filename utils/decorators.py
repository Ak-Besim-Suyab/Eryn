import discord
import time
from functools import wraps

def cooldown(seconds: float = 3.0):
    """
    定義冷卻時間裝飾器，技能在施放前都須要判斷是否在冷卻時間內，屬於外圍判定，因此設計此裝飾器
    這個裝飾器專門用於帶有實例方法的類別，特別是 Action 類別，否則會報錯
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
            now = time.time()
            if interaction.user.id in self.timestamps:
                elapsed = now - self.timestamps[interaction.user.id]
                if elapsed < seconds:
                    remaining = seconds - elapsed
                    await interaction.response.send_message(f"❌ 技能冷卻中，請等待 {remaining:.1f} 秒後再試。", ephemeral=True)
                    return
                
            self.timestamps[interaction.user.id] = now
            return await func(self, interaction, *args, **kwargs)
            
        return wrapper
    
    return decorator