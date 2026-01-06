# services/logger.py
# Lightweight logger using print or loguru if available

try:
    from loguru import logger as loguru_logger
    loguru_logger.add("logs/insightiq.log", rotation="10 MB", retention="7 days", enqueue=True)
    def get_logger():
        return loguru_logger
except Exception:
    import logging
    logging.basicConfig(level=logging.INFO)
    def get_logger():
        return logging.getLogger("insightiq")

