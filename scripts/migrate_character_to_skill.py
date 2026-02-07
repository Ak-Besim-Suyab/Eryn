from database.generic import db
from database.character import Character
from database.skill import Skill


CHARACTER_SKILL_NAME = "character"


def migrate_character_to_skill():
    with db.atomic():
        for character in Character.select():
            skill, _ = Skill.get_or_create(
                player_id=character.player_id,
                name=CHARACTER_SKILL_NAME,
            )
            skill.level = character.level
            skill.experience = character.experience
            skill.save()


if __name__ == "__main__":
    migrate_character_to_skill()
    print("✅ 已將 Character 資料轉移到 Skill(name='character')。")
