import logging

def logger():
    # Configure the root logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Create a logger for this module and return it
    return logging.getLogger(__name__)

# Use the logger
logger = logger()