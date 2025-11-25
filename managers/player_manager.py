from models.player import Player

class PlayerManager:
    def __init__(self):
        self.players = {}
        print("[PlayerManager] Manager loaded.")

    def get_player(self, interaction):
        uid = interaction.user.id
        name = interaction.user.display_name

        if uid not in self.players:
            player = Player(uid, name)
            player.restore_data()
            self.players[uid] = player
            print(f"[PlayerManager] User data {name} not found, now registered.")
        else:
            print(f"[PlayerManager] User data {name} existed.")
        return self.players[uid]

    def remove_player(self, uid):
        self.players.pop(uid, None)