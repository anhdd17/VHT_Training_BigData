import logging


LOG_FORMAT = "{levelname: <8}:{asctime}:{name: <30}:{lineno: <4}:{message}"
logging.basicConfig(filename="logs/etl.log", format=LOG_FORMAT, level=logging.INFO, style="{")
Logger = logging.getLogger("etl")

