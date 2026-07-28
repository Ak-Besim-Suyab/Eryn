from models.statistic import Statistic
from models.player import Player

Statistic.ensure_schema()
print('schema ok')
p = Player.get_or_create_player(999999)
print('player ok', p.id)
s = Player.get_stat(999999)
print('stat ok', s.id, s.display_name, s.total_message_send)
