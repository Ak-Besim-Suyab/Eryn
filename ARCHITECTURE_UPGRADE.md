# 升級系統架構變更記錄

## 📋 變更日期
2026-01-19

## 🎯 核心改動

### 之前的架構（已移除）
```
database/
└── level_system.py
    ├── Level 模型（通用表）
    │   ├── player_id
    │   ├── system_type （"character", "fishing", "mining"）
    │   ├── level
    │   └── experience
```

**問題：**
- 語義不清：character 和 skill 混在同一張表
- 難以擴展：無法為不同系統添加專屬屬性
- 刪除系統困難：影響整個 Level 表

---

### 新架構（現已實施）
```
database/
├── character.py
│   └── Character 模型
│       ├── player_id (ForeignKey)
│       ├── level
│       ├── experience
│       └── 方法：add_experience(), get_progress()
│
└── skill.py
    └── Skill 模型
        ├── player_id (ForeignKey)
        ├── skill_type ("fishing", "mining", "cooking" 等)
        ├── level
        ├── experience
        └── 方法：add_experience(), get_progress(), get_all_skills()
```

**優勢：**
- ✅ 語義清晰：Character 專門用於角色等級，Skill 用於技能
- ✅ 易於擴展：未來可為 Skill 添加 `cooldown`、`success_rate` 等屬性
- ✅ 易於刪除：想刪除某個技能系統時，只需刪除對應 skill_type 的記錄
- ✅ 靈活性高：不同系統可有完全不同的升級邏輯

---

## 🔄 遷移詳情

### 文件變更
1. **新增：** `database/character.py` - 角色等級系統
2. **新增：** `database/skill.py` - 技能系統基礎（釣魚、挖礦）
3. **修改：** `database/__init__.py` - 更新初始化順序
4. **修改：** `cogs/leveling.py` - 導入和方法調用更新
5. **修改：** `test_level_system.py` - 測試更新
6. **修改：** `test_leveling.py` - 測試更新
7. **刪除：** `database/level_system.py` - 已被 character.py 和 skill.py 替代

### 初始化順序
```python
init_all_databases()
  ├── 1️⃣ Player 表（核心）
  ├── 2️⃣ Dummy 表（獨立）
  ├── 3️⃣ Affection 表（依賴 Player + Dummy）
  ├── 4️⃣ Character 表（依賴 Player - 角色等級）
  └── 5️⃣ Skill 表（依賴 Player - 技能等級）
```

---

## 📊 數據庫架構

### Character 表
```sql
CREATE TABLE character (
  id INTEGER PRIMARY KEY,
  player_id INTEGER UNIQUE NOT NULL,
  level INTEGER DEFAULT 1,
  experience INTEGER DEFAULT 0,
  FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE
)
```

### Skill 表
```sql
CREATE TABLE skill (
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL,
  skill_type TEXT NOT NULL,
  level INTEGER DEFAULT 1,
  experience INTEGER DEFAULT 0,
  UNIQUE (player_id, skill_type),
  FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE
)
```

---

## 🎮 玩家互動流程

### 訊息經驗（現有）
```
玩家發送訊息
  ↓
@on_message 監聽
  ↓
檢查冷卻時間（30秒）
  ↓
Character.add_experience(user_id, 5)
  ↓
檢查升級 → 廣播通知
```

### 語音經驗（現有）
```
玩家加入語音
  ↓ （記錄時間戳）
玩家離開語音
  ↓ （計算停留時間）
Character.add_experience(user_id, exp)
  ↓
檢查升級 → 廣播通知
```

### 技能經驗（為未來準備）
```
玩家進行技能行為（釣魚、挖礦）
  ↓
Skill.add_experience(user_id, exp, skill_type)
  ↓
檢查升級 → 廣播通知
```

---

## ✅ 測試驗證

### 測試結果
```
✅ test_level_system.py - 7 個測試全部通過
✅ test_leveling.py - 7 個測試全部通過
✅ 機器人啟動測試 - 成功登入和同步指令
```

### 驗證項目
- ✅ Character 系統初始化
- ✅ Skill 系統初始化
- ✅ 訊息經驗增加邏輯
- ✅ 升級檢測和通知
- ✅ 進度查詢功能
- ✅ 語音時間計算
- ✅ 冷卻時間檢查
- ✅ 多技能支持

---

## 🚀 未來擴展例子

### 添加釣魚系統
```python
# 簡單！只需在需要的地方調用：
result = Skill.add_experience(user_id, exp, "fishing")

# 未來可添加技能專屬屬性：
class Skill(Model):
    skill_type = TextField()
    cooldown = IntegerField(default=0)  # 技能冷卻時間
    success_rate = FloatField(default=100)  # 成功率
```

### 添加烹飪系統
```python
# 同樣的方式：
Skill.add_experience(user_id, exp, "cooking")
```

### 添加角色屬性
```python
# Character 可添加角色專屬屬性：
class Character(Model):
    class_type = TextField()  # "warrior", "mage" 等
    health = IntegerField()
    mana = IntegerField()
    # 等等...
```

---

## 📝 查詢指令

### 當前支持的指令
```
!等級                  - 查看自己的角色等級
!等級 @玩家            - 查看指定玩家的角色等級
!排行榜                - 查看角色等級排行榜
```

### 未來技能查詢指令（待實現）
```
!釣魚等級              - 查看釣魚技能等級
!挖礦等級              - 查看挖礦技能等級
!技能排行榜 釣魚       - 查看釣魚等級排行榜
```

---

## 💡 設計優勢總結

| 方面 | 舊架構（通用表） | 新架構（分離表） |
|------|-----------------|-----------------|
| 語義清晰度 | ❌ 模糊 | ✅ 清晰 |
| 擴展性 | ❌ 困難 | ✅ 簡單 |
| 系統刪除 | ❌ 複雜 | ✅ 簡單 |
| 屬性靈活性 | ❌ 受限 | ✅ 高 |
| 代碼可讀性 | ❌ 低 | ✅ 高 |
| 查詢效率 | ✅ 相同 | ✅ 相同 |

---

## 🎓 學習重點

本次架構優化展示了以下設計原則：

1. **單一責任原則**：每個模型只負責一個責任
2. **開閉原則**：對擴展開放，對修改關閉
3. **語義清晰**：代碼自註釋，易於理解
4. **未來考量**：設計時考慮可能的擴展方向




# 開發者筆記

### 目錄分層

cores   : 抽象層，負責讀取、輸出器等底層邏輯
models  : 資料層，負責資料庫與基礎結構定義
systems : 運算層，負責組織業務邏輯，從抽象或資料層級撈取需要的資料並執行運算
views   : 視覺層，負責調用運算相關層級的業務邏輯執行運算，獲取結果後組裝並輸出
utils   : 工具層，負責最外部的額外運算或插入邏輯，比如裝飾器、單位轉換