from os import path, remove
import logging

if path.isfile("logs/logs.log"):
    remove("logs/logs.log")
 
# Create the Logger
logger = logging.getLogger('meGlobalLogger')
logger.setLevel(logging.DEBUG)
 

#Handler for console
console_logger = logging.StreamHandler()
 
# Create a Formatter for formatting the log messages
format = logging.Formatter('%(levelname)s : %(asctime)-15s : %(message)s', '%d/%m/%Y %I:%M:%S %p')

# Add the Formatter to the Handlers
console_logger.setFormatter(format)
 
# Add the Handler to the Logger
logger.addHandler(console_logger)
