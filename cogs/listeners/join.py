import asyncio
import discord
from discord.ext import commands

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_message = [
            "咪，很高興旅人來到避風港 🎉",
            "這裡是個溫暖、可愛的小地方，希望您會喜歡喵！"
        ]

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        # 忽略機器人加入事件
        if member.bot:
            return
        
        await self.send_welcome_message(member)
        await self.send_direct_message(member)


    async def send_welcome_message(self, member: discord.Member):
        channel = member.guild.system_channel

        if channel:
            try:
                async with channel.typing():
                    await asyncio.sleep(10.0)
                    await channel.send(f"咪！歡迎 {member.mention} 加入喵！")
                    
            except discord.Forbidden:
                print(f"無法傳送歡迎訊息給 {member.name}（私訊已關閉）")

    async def send_direct_message(self, member: discord.Member):
        try:
            dm_channel = await member.create_dm()
            for msg in self.welcome_message:
                async with dm_channel.typing():
                    await asyncio.sleep(5.0)
                    await member.send(msg)
            
            view = JoinView()
            await asyncio.sleep(5.0)
            await member.send("咪可以在這裡回答一些簡單的問題，如果旅人感興趣的話，可以按按鈕問問咪！", view=view)

        except discord.Forbidden:
            print(f"無法傳送歡迎訊息給 {member.name}（私訊已關閉）")
        
class JoinView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="你是誰？", style=discord.ButtonStyle.secondary, emoji="🐱")
    async def intruduce_self(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = [
            "很高興認識您，咪是... 避風港的小管家喵！",
            "咪負責... 咪負責很多東西",
            "像是跟新加入的旅人打招呼、介紹避風港的特色、幫旅人設定身分組和自介，還有... 還有... 回答旅人的問題",
            "但是，由於咪還在開發中，部分功能可能無法使用或尚未完善，還請旅人多多回饋與包涵喵！"
        ]

        await interaction.response.defer()

        for msg in message:
            async with interaction.channel.typing():
                await asyncio.sleep(5.0)
                await interaction.channel.send(msg)

    @discord.ui.button(label="避風港是個什麼樣的社群呢？", style=discord.ButtonStyle.secondary, emoji="🐱")
    async def intruduce_community(self, interaction: discord.Interaction, button: discord.ui.Button):
        messages = [
            "咪，避風港是個綜合向遊戲社群！",
            "旅人可以在這裡尋找擁有共同興趣的小夥伴、和大家一起玩遊戲、討論動漫電影，以及分享自己的生活喵！",
            "我們會不定期舉辦一些活動，像是揪團看電影、小遊戲派對，還有... 各式各樣的線上或線下聚會！",
        ]

        await interaction.response.defer() 

        for msg in messages:
            async with interaction.channel.typing():
                await asyncio.sleep(5.0)
                await interaction.channel.send(msg)

    
    @discord.ui.button(label="可以摸摸咪嗎？", style=discord.ButtonStyle.secondary, emoji="🐱")
    async def pet_cat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer() 
        await interaction.channel.send("咪！ \n-# *\*開心地搖尾巴\**")

async def setup(bot):
    await bot.add_cog(Join(bot))