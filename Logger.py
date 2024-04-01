import requests, time, logging, colorlog

# Create a logger
logger = colorlog.getLogger()
logger.setLevel(logging.DEBUG)

# Create a handler
handlerLog = colorlog.StreamHandler()
handlerLog.setFormatter(
    colorlog.ColoredFormatter(
        "[%(asctime)s] - %(log_color)s%(levelname)s:%(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
)
logger.addHandler(handlerLog)
