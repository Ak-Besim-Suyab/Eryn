from database.generic import db
from database.character import Character
from database.skill import Skill


def merge_character_skill_db():
    with db:
        db.create_tables([Character, Skill], safe=True)


if __name__ == "__main__":
    merge_character_skill_db()
    print("✅ Character 與 Skill 資料表已建立/合併完成。")
