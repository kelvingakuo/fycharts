from os import path, remove
import logging

if path.isfile("logs/logs.log"):
    remove("logs/logs.log")
 
# Create the Logger
logger = logging.getLogger('meGlobalLogger')
logger.setLevel(logging.DEBUG)
 
# Create the Handler for logging data to a file
file_logger = logging.FileHandler('logs/logs.log')

#Handler for console
console_logger = logging.StreamHandler()
 
# Create a Formatter for formatting the log messages
format = logging.Formatter('%(levelname)s : %(asctime)-15s : %(message)s', '%d/%m/%Y %I:%M:%S %p')

# Add the Formatter to the Handlers
file_logger.setFormatter(format)
console_logger.setFormatter(format)
 
# Add the Handler to the Logger
logger.addHandler(file_logger)
logger.addHandler(console_logger)
