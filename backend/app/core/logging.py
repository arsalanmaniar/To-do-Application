import logging
from typing import Optional


def setup_logging(log_level: Optional[str] = "INFO"):
    """
    Setup logging configuration for the application
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Get the logger for this application
    logger = logging.getLogger(__name__)
    return logger


# Create a default logger instance
logger = setup_logging()