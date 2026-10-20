import datetime

def get_formatted_time() -> str:
    now = datetime.datetime.now()
    ampm = "上午" if now.hour < 12 else "下午"

    return f"{now.year}/{now.month}/{now.day} {ampm} {now.strftime('%I:%M')}"