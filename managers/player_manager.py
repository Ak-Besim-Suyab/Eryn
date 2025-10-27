from models.player import Player

class PlayerManager:
    def __init__(self):
        self.players = {}
        print("[PlayerManager] Manager loaded.")

    def get_player(self, interaction):
        ID = interaction.user.id
        name = interaction.user.display_name

        if ID not in self.players:
            self.players[ID] = Player(ID, name)
            print(f"[PlayerManager] User data {name} not found, now registered.")
        else:
            print(f"[PlayerManager] User data {name} exsisted.")
        return self.players[ID]

    def remove_player(self, ID):
        self.players.pop(ID, None)