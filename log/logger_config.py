# logger_config.py
import sys
from loguru import logger

def setup_logging():
    """
    Sets up the centralized logging configuration using Loguru.
    This function should be called once at the application's startup.
    """
    # Remove default handler to prevent duplicate logs if you reconfigure
    logger.remove()

    # Add a sink for console output
    logger.add(
        sys.stderr,
        level="INFO", # Default level for console
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        diagnose=True # Show variable values in traceback for exceptions
    )

    # Add a sink for file output (e.g., rotating log file)
    logger.add(
        "log/logs.log",
        level="DEBUG", # More detailed level for file
        rotation="10 MB",  # Rotate file every 10 MB
        compression="zip", # Compress old log files
        retention="7 days", # Keep logs for 7 days
        enqueue=True,      # Use a queue for non-blocking writes (important for performance)
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        diagnose=True
    )

    # You can add more sinks as needed, e.g., for error logs only, or specific modules
    logger.add(
        "log/error.log",
        level="ERROR", # Only log ERROR and above to this file
        rotation="1 week",
        compression="zip",
        retention="4 weeks",
        enqueue=True,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        diagnose=True
    )

    # You can also set a global minimum level if desired, but sinks override this.
    # logger.level("INFO") # Set global minimum level

    # Return the configured logger instance (though it's a global singleton,
    # returning it can be good practice for clarity)
    return logger

# Call setup_logging immediately when this module is imported
# This ensures logging is configured as soon as your app starts importing modules.
configured_logger = setup_logging()

# You can now import 'configured_logger' from this file in other modules.
# For convenience, you might re-export the global 'logger' from loguru
# after configuration, or just use 'configured_logger'.
# For simplicity, we'll just use `from loguru import logger` directly in other files
# after this setup is run.