import re

emoji_pattern = re.compile(r"<a?:\w+:(\d+)>")

def count_emoji(content: str, emoji_id: str) -> int:
    return emoji_pattern.findall(content).count(emoji_id)