import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(log_dir="logs", filename="app.log"):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = os.path.join(log_dir, filename)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    # File log handler con rotazione
    file_handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console log handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Logger principale
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Disabilita doppio logging per Werkzeug
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
