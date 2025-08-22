"""
Logging utilities for Vantage AI PersonaPilot
"""

import logging
import sys
from typing import Optional
from .config import Config

def setup_logger(name: str = "vantage_ai", 
                level: Optional[str] = None,
                config: Optional[Config] = None) -> logging.Logger:
    """
    Setup and configure logger
    
    Args:
        name: Logger name
        level: Log level (if not provided, uses config)
        config: Configuration object
        
    Returns:
        Configured logger
    """
    if config is None:
        config = Config()
    
    log_level = level or config.log_level
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Avoid adding handlers if they already exist
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Create file handler for debug mode
    if config.debug:
        file_handler = logging.FileHandler('vantage_ai.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str = "vantage_ai") -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)

