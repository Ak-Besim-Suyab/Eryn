import datetime

from config import timezone

hour = datetime.time(hour=12, minute=0, tzinfo=timezone)

print(hour)