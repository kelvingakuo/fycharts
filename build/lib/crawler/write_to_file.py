import pandas as pd

from log_config import logger


def writeToCSV(j, output_file, df):
	if(j == 0):
		isHeaders = True
	else:
		isHeaders = False

	with open(output_file, 'a') as out:
		logger.info('Appending data to {}...'.format(output_file))
		df.to_csv(out, index = False, header = isHeaders)
		logger.info('Done writing to {}!!!'.format(output_file))