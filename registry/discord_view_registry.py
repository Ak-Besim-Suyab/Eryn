from managers.discord_view_manager import DiscordViewManager

from ui.views.fishing_view import FishingView

discord_view_manager = DiscordViewManager()

# 註冊所有 View
discord_view_manager.register("fishing_view", FishingView)