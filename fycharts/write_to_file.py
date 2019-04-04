import pandas as pd

from .log_config import logger


def writeToCSV(j, output_file, df):
	if(j == 0):
		isHeaders = True
	else:
		isHeaders = False

	with open(output_file, 'a', encoding='utf-8') as out:
		logger.info('Appending data to {}...'.format(output_file))
		df.to_csv(out, index = False, header = isHeaders, encoding = 'utf-8')
		logger.info('Done writing to {}!!!'.format(output_file))