# cogs/listeners/threads_embed_fix.py
import re
import json
import html
import aiohttp
import discord
from discord.ext import commands

from cores.logger import logger

THREADS_PATTERN = re.compile(
    r"https?://(?:www\.)?threads\.(?:net|com)/@([\w.\-]+)/post/([\w\-]+)(?:\?\S*)?"
)

REQUEST_HEADERS = {
    "User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"
}

META_TAG_PATTERN = re.compile(r"<meta\s+[^>]*>", re.IGNORECASE)
ATTR_PATTERN = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')

# 抓取內嵌在頁面裡的結構化資料 (data-sjs script block)
SJS_SCRIPT_PATTERN = re.compile(
    r'<script type="application/json"[^>]*data-sjs[^>]*>(.*?)</script>',
    re.DOTALL,
)


def parse_og_tags(page_html: str) -> dict:
    data = {}
    for tag in META_TAG_PATTERN.findall(page_html):
        attrs = dict(ATTR_PATTERN.findall(tag))
        key = attrs.get("property") or attrs.get("name")
        content = attrs.get("content")
        if key and key.startswith("og:") and content:
            data[key] = html.unescape(content)
    return data


def find_key(data, target_key: str):
    """
    遞迴搜尋巢狀 dict/list，回傳第一個符合 target_key 且不為 None 的值
    用於解析 Threads 內嵌的結構化資料，避免寫死巢狀路徑
    """
    if isinstance(data, dict):
        if target_key in data and data[target_key] is not None:
            return data[target_key]
        for value in data.values():
            result = find_key(value, target_key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key(item, target_key)
            if result is not None:
                return result
    return None


def parse_engagement_data(page_html: str) -> dict:
    """
    掃描頁面內所有 data-sjs script block，嘗試解析出互動數據與作者頭像
    每個 block 各自嘗試 json.loads，失敗的直接跳過（頁面裡有很多不相關的 script block）
    """
    result = {}

    for raw in SJS_SCRIPT_PATTERN.findall(page_html):
        try:
            blob = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            continue

        if "profile_pic_url" not in result:
            avatar = find_key(blob, "profile_pic_url")
            if avatar:
                result["profile_pic_url"] = avatar

        if "like_count" not in result:
            likes = find_key(blob, "like_count")
            if likes is not None:
                result["like_count"] = likes

        if "reply_count" not in result:
            replies = find_key(blob, "reply_count") or find_key(blob, "view_replies_cta_string")
            if replies is not None:
                result["reply_count"] = replies

        if "reshare_count" not in result:
            reposts = find_key(blob, "reshare_count") or find_key(blob, "repost_count")
            if reposts is not None:
                result["reshare_count"] = reposts

    return result


def _extract_number(value) -> str | None:
    """有些欄位是字串形式，例如 '70 replies'，這裡抓出數字部分"""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return str(int(value))
    match = re.search(r"[\d,]+", str(value))
    return match.group(0) if match else None


class ThreadsEmbedFixCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session: aiohttp.ClientSession | None = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession(headers=REQUEST_HEADERS)

    async def cog_unload(self):
        if self.session:
            await self.session.close()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        matches = list(THREADS_PATTERN.finditer(message.content))
        if not matches:
            return

        sent_any = False
        for match in matches:
            username = match.group(1)
            url = match.group(0)

            page_html = await self._fetch_html(url)
            if page_html is None:
                continue

            og_data = parse_og_tags(page_html)
            if not og_data.get("og:description") and not og_data.get("og:image"):
                logger.debug(f"Threads 貼文沒有可用的 OG 資料: {url}")
                continue

            engagement = parse_engagement_data(page_html)

            embed = self._build_embed(url, username, og_data, engagement)
            await message.reply(embed=embed, mention_author=False)
            sent_any = True

        if sent_any:
            await self._suppress_original(message)

    async def _fetch_html(self, url: str) -> str | None:
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                if resp.status != 200:
                    logger.warning(f"抓取 Threads 貼文失敗，狀態碼: {resp.status}，URL: {url}")
                    return None
                return await resp.text()
        except Exception as e:
            logger.warning(f"抓取 Threads 貼文時發生錯誤: {e}")
            return None

    def _build_embed(self, url: str, username: str, og_data: dict, engagement: dict) -> discord.Embed:
        embed = discord.Embed(
            description=og_data.get("og:description", ""),
            color=discord.Color.dark_theme(),
            url=url,
        )

        embed.set_author(
            name=f"@{username}",
            icon_url=engagement.get("profile_pic_url"),
            url=url,
        )

        if image := og_data.get("og:image"):
            embed.set_image(url=image)

        stats = []
        if (likes := _extract_number(engagement.get("like_count"))) is not None:
            stats.append(f"❤️ {likes}")
        if (replies := _extract_number(engagement.get("reply_count"))) is not None:
            stats.append(f"💬 {replies}")
        if (reposts := _extract_number(engagement.get("reshare_count"))) is not None:
            stats.append(f"🔁 {reposts}")

        embed.set_footer(text="  ".join(stats) if stats else "Threads")

        return embed

    async def _suppress_original(self, message: discord.Message):
        try:
            if message.guild and message.channel.permissions_for(message.guild.me).manage_messages:
                await message.edit(suppress=True)
        except (discord.Forbidden, discord.HTTPException) as e:
            logger.warning(f"無法抑制原始 embed: {e}")


async def setup(bot):
    await bot.add_cog(ThreadsEmbedFixCog(bot))