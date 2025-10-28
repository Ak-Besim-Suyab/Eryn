import sqlite3
import os

from context import Context

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "player_data.db")

class Database:
    def __enter__(self):
        self.conn = sqlite3.connect(DATA_PATH)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

class SkillRegistry:
    def register(self):
        skill_data = {"ID": "INTEGER PRIMARY KEY"}
        skills = Context.get_skill_entry()

        for name in skills:
            skill_level = f"{name}_level"
            skill_experience = f"{name}_experience"

            skill_data[skill_level] = f"INTEGER DEFAULT 1"
            skill_data[skill_experience] = f"INTEGER DEFAULT 0"

        return skill_data

class DataManager:
    def __init__(self):
        self.data = {}

    def load_database(self):
        loader = Context.loader

        # data registry, register new data here.
        self.data["players"] = loader.load("data/players")
        self.data["items"] = loader.load("data/items")
        self.data["skills"] = SkillRegistry().register()

        for name in self.data:
            self.create_database(name)
            self.complete_database(name)

        print("[DataManager] Manager loaded.")

    def load_player_data(self, player: object):
        self.check_player_database(player)
        self.load_player_database(player)

    #--- create database if it is not exsisted.
    #--- this is a framework creating ensuring data can be stored somewhere, not really a "storing data" function
    def create_database(self, name):
        with Database() as c:
            data_table = ", ".join(f"{key} {value}" for key, value in self.data[name].items())
            c.execute(f"CREATE TABLE IF NOT EXISTS {name} ({data_table})")

            print(f"[DataManager] {name}'s database created.")

    #--- register new column if function found, pass if no column new.   
    def complete_database(self, name):
        with Database() as c:
            existing_data = [col[1] for col in c.execute(f"PRAGMA table_info({name})").fetchall()]

            for d in self.data[name]:
                if d not in existing_data:
                    try:
                        c.execute(f"ALTER TABLE {name} ADD COLUMN {d} {self.data[name][d]}")
                        print(f"[DataManager] Found new column {d} in {name}, registered.")
                    except sqlite3.OperationalError as e:
                        print(f"[DataManager] Cannot add {d} column in {name}: {e}")

    #--- check if table with player is exsisted, and set all values default, where value is (?)
    def check_player_database(self, player: object):
        with Database() as c:
            for name in self.data:
                c.execute(f"INSERT OR IGNORE INTO {name} (ID) VALUES (?)", (player.ID,))

                print(f"{player.ID}'s {name} data checked successfully.")

    #--- load data in database.
    def load_player_database(self, player: object):
        with Database() as c:
            for name, data in self.data.items():
                # catch 'name' in column of data
                cols = [col for col in data if col != "ID"] 
                cols_str = ", ".join(cols)

                # catch 'value' in column of data
                c.execute(f"SELECT {cols_str} FROM {name} WHERE ID = ?", (player.ID,)) 
                row = c.fetchone()

                print(f"[DataManager] {name} data loaded: {row}")
                print(f"[DataManager] now insert in {player.name}'s {name} data..")

                if row:
                    for i, col in enumerate(cols):
                        match name:
                            case "players":
                                setattr(player, col, row[i])
                            case "items":
                                player.inventory.set_item(col, row[i])
                            case "skills":
                                if "_" in col:
                                    skill_name, attr = col.split("_", 1)
                                    skill_obj = getattr(player.skill, skill_name, None)
                                    if skill_obj:
                                        setattr(skill_obj, attr, row[i])
                                    else:
                                        print(f"[Warning] Skill '{skill_name}' not found in player.skill")

                print(f"[DataManager] {player.name}'s {name} data done!")

    #--- save data in database.
    def save_data(self, name: str, ID: int, data: dict):
        with Database() as c:
            update_columns = ", ".join(f"{key}=?" for key in data.keys())
            update_values = list(data.values())
            update_values.append(ID)

            c.execute(f"UPDATE {name} SET {update_columns} WHERE ID=?", update_values)