from managers.button_manager import ButtonManager
from ui.buttons.community_rule_button import CommunityRuleButton

button_manager = ButtonManager()

# 註冊所有按鈕
button_manager.register("community_rule_button", CommunityRuleButton)