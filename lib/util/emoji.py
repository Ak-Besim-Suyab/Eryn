import re

emoji_pattern = re.compile(r"<a?:\w+:(\d+)>")

def count(content: str, emoji_id: str) -> int:
    return emoji_pattern.findall(content).count(emoji_id)