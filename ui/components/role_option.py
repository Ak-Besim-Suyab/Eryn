import discord

from context import Context

from utils.logger import logger

class RoleOption(discord.ui.Select):
    def __init__(self, session, player, role_tag, role_data):
        self.session = session
        self.player = player
        self.role_tag = role_tag
        self.role_data = role_data

        options = []
        for role_id, data in self.role_data.items():
            flags = data.get("flags", {})
            display_name = data.get("display_name", role_id)

            # 如果該身分組是 default, 或玩家背包有該身分組道具, 則標記為可套用; 如果都沒有, 則標記為無法套用
            if flags.get("is_default") or self.player.has_item(role_id):
                description = "選擇後會套用身分組"
            else:
                description = "你尚未擁有該身分組，無法套用"

            options.append(
                discord.SelectOption(
                    label=f"{display_name}",
                    description=description,
                    value=role_id
                )
            )
        super().__init__(
            placeholder="選擇你想要套用的身分組",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected_role = self.values[0]
        data = self.role_data.get(selected_role) # 這裡從得到的身分組使用 string id 取出資料
        if not data:
            await interaction.response.send_message("❌ 找不到該身分組資料，請聯絡管理員處理。", ephemeral=True)
            logger.error(f"找不到身分組資料：{selected_role}")
            return

        role_id = data.get("role_id")
        if not role_id:
            await interaction.response.send_message("❌ 身分組資料缺少 role_id，請聯絡管理員處理。", ephemeral=True)
            logger.error(f"身分組資料缺少 role_id：{selected_role}")
            return
        guild_role = interaction.guild.get_role(role_id)

        # 檢查身分組是否存在
        if not guild_role:
            await interaction.response.send_message("❌ 伺服器內找不到該身分組，請聯絡管理員處理。", ephemeral=True)
            return
        
        # 檢查使用者是否已經有該身分組
        if guild_role in interaction.user.roles:
            await interaction.response.send_message(f"❌ 你已經套用該身分組。", ephemeral=True)
            return
        
        try:
            # 檢查玩家是否有權限套用此身分組
            is_default = data.get("flags", {}).get("is_default", False)
            has_item = self.player.has_item(selected_role)
            
            if not is_default and not has_item:
                await interaction.response.send_message("❌ 你尚未擁有該身分組，無法套用。", ephemeral=True)
                return
            
            # 先加入新身分組
            await interaction.user.add_roles(guild_role, reason="使用者透過指令自行套用身分組。")
            
            # 移除同分類的其他身分組（不移除剛加入的）
            removed_roles = Context.get_manager("item").get_items_by_tag([self.role_tag])
            for removed_role_id, removed_role_data in removed_roles.items():
                removed_role_id = removed_role_data["role_id"]
                # 跳過剛加入的身分組
                if removed_role_id == role_id:
                    continue
                
                other_guild_role = interaction.guild.get_role(removed_role_id)
                if other_guild_role and other_guild_role in interaction.user.roles:
                    await interaction.user.remove_roles(other_guild_role, reason="相同分類的身分組同時只能套用 1 個。")
            
            await interaction.response.send_message(
                content = f"✅ 成功套用身分組 <@&{role_id}>！", 
                allowed_mentions=discord.AllowedMentions(roles=False), 
                ephemeral=True
            )

        except discord.Forbidden:
            # 沒有權限時拋出回應
            await interaction.response.send_message("❌ 機器人沒有權限套用該身分組，請聯絡管理員檢查。", ephemeral=True)
            logger.error("機器人沒有權限套用身分組")
            return
        except Exception as e:
            # 其他錯誤時拋出回應
            await interaction.response.send_message("❌ 套用身分組時發生錯誤，請聯絡管理員檢查。", ephemeral=True)
            logger.error(f"套用身分組時發生錯誤：{e}")