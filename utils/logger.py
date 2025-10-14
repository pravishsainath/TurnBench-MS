import logging
import sys

logging_level_mapping = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Sets up and returns a configured logger."""
    # Prevent multiple handlers if called multiple times
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger # Logger already configured

    logger.setLevel(level)

    # Create console handler and set level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    return logger

def get_logging_level(log_level: str) -> int:
    """Get logging level from string"""
    return logging_level_mapping.get(log_level, logging.INFO)