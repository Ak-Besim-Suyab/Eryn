from context import Context

class Skill:
    def __init__(self, ID: str, name: str, base = 45, multipler = 1.285, bonus = 18):
        self.ID = ID
        self.name = name
        self.level = 1
        self.experience = 0

        # formula parameter
        self.base = base
        self.multipler = multipler
        self.bonus = bonus

    # function of experience formula.
    def require_exp(self):
        return int(self.base * (self.level ** self.multipler) + self.level * self.bonus)

    def process_leveling(self):
        require_exp = self.require_exp()
        old_level = self.level

        if self.experience >= require_exp:
            while self.experience >= require_exp:
                self.experience -= require_exp
                self.level += 1
            new_level = self.level
            return { "skill_name": self.name, "old_level": old_level, "new_level": new_level }
        else:
            return None

class SkillContainer(Skill):
    def __init__(self, ID: int):
        self.ID = ID
        self.skills = Context.get_skill_entry()

        for skill_id, skill_name in self.skills.items():
            if skill_id == "character":
                setattr(self, skill_id, Skill(ID = skill_id, name = skill_name, base = 80, multipler = 1.375, bonus = 30))
            else:
                setattr(self, skill_id, Skill(ID = skill_id, name = skill_name))

    def process_all_leveling(self, *entry):
        leveling_result = []
        for skill_id in self.skills:
            process_result = getattr(self, skill_id).process_leveling()
            if process_result:
                leveling_result.append(process_result)

        return leveling_result

