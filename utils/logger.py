import logging
import os
from datetime import datetime
 
from logging.handlers import TimedRotatingFileHandler

os.makedirs("logs", exist_ok=True)

log_filename = f"logs/bot_{datetime.now().strftime('%Y-%m-%d')}.log"

logger = logging.getLogger("Eryn")
logger.setLevel(logging.DEBUG)  

formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

time_rotating_handler = TimedRotatingFileHandler(
    filename="logs/bot.log",
    when="midnight",     
    interval=1,          
    backupCount=7,       
    encoding="utf-8"
)
time_rotating_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(time_rotating_handler)

# How to use logger:
#
# logger.info("Bot starting..")
# logger.debug("This is a debug message.")
# logger.warning("warning: data type is wrong.")
# logger.error("error: cannot connect to database.")
# logger.critical("critical error happened, system will be shut down soon.")