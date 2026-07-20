"""
Module: logger.py


Purpose:
Configure application logging for the entire application.

Responsibilities:
- Configure logging once
- Log messages to terminal
- Log messages to app.log
"""

import logging
level = logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)