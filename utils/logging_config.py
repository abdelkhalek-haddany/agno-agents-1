import logging

def setup_logging():
    """Set up logging for the application"""
    logger = logging.getLogger("AgnoUnifiedAgent")
    logger.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)

    # Add handler to logger (if not already added)
    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger
