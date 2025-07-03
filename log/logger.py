from loguru import logger

# Configure Loguru for logging
logger.add(
    "log/logs.log",
    rotation="10 MB",  # Rotate the log file when it reaches 10 MB
    retention="7 days",  # Keep logs for 7 days
    enqueue=True,      # Make logging non-blocking
    backtrace=True,    # Show full stack traces
    level=1,      # Set the minimum level to log
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
)
