from model import Player

player, _ = Player.get_or_create(id=1)

print(player.turn)