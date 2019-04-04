import datetime
import pandas as pd
import random
import sys
import time

from .crawler_base import SpotifyChartsBase
from .compute_dates import returnDatesAndRegions
from .log_config import logger
from .write_to_file import writeToCSV



def validateFile(fileName):
	if('csv' in fileName):
			file = fileName

			return file
	else:
		logger.error('ONLY CSV EXTENSIONS ALLOWED!!!')
		sys.exit(0)

	

# Class definition
class SpotifyCharts(SpotifyChartsBase):
	def __init__(self):
		SpotifyChartsBase.__init__(self)

	def top200Weekly(self, output_file, start=None, end=None, region=None):
		"""Write to file the charts data for top 200 weekly
		output_file - CSV file to write the data to
		start - Start of range (YYYY-MM-DD) as string
		end - End of range (YYYY-MM-DD) as string
		region - Region to get data for

		* Any parameter passed as None, means ALL data since the beginning up to now
		"""
		file = validateFile(output_file)
		data = returnDatesAndRegions(start, end, region, isWeekly=True, isViral=False)

		dates = data['dates']
		regions = data['region']

		j = 0
		while(j < len(dates)):
			if((j + 1) == len(dates)): 
				break
			theRange = dates[j]+'--'+dates[j+1]

			for region in regions:
				self.logger.info('Extracting top 200 weekly for {} - {}'.format(theRange, region))
				df = super().getTop200Weekly(theRange, region)

				writeToCSV(j, file, df)
				time.sleep(random.randint(0, j))
			j = j + 1


	def top200Daily(self, output_file, start=None, end=None, region=None):
		"""Write to file the charts data for top 200 daily
		output_file - CSV file to write the data to
		start - Start of range (YYYY-MM-DD) as string
		end - End of range (YYYY-MM-DD) as string
		region - Region to get data for

		* Any parameter passed as None, means ALL data since the beginning up to now
		"""
		file = validateFile(output_file)
		data = returnDatesAndRegions(start, end, region, isWeekly=False, isViral=False)

		dates = data['dates']
		regions = data['region']

		j = 0
		while(j < len(dates)):
			theRange = dates[j]

			for region in regions:
				self.logger.info('Extracting top 200 daily for {} - {}'.format(theRange, region))
				df = super().getTop200Daily(theRange, region)

				writeToCSV(j, file, df)
				time.sleep(random.randint(0, j))

			j = j + 1

	def viral50Weekly(self, output_file, start=None, end=None, region=None):
		"""Write to file the charts data for viral 50 weekly
		output_file - CSV file to write the data to
		start - Start of range (YYYY-MM-DD) as string
		end - End of range (YYYY-MM-DD) as string
		region - Region to get data for

		* Any parameter passed as None, means ALL data since the beginning up to now
		"""
		file = validateFile(output_file)
		data = returnDatesAndRegions(start, end, region, isWeekly=True, isViral=True)

		dates = data['dates']
		regions = data['region']

		j = 0
		while(j < len(dates)):
			if((j) == len(dates)): 
				break
			theRange = dates[j]+'--'+dates[j]

			for region in regions:
				self.logger.info('Extracting viral 50 weekly for {} - {}'.format(theRange, region))
				df = super().getViral50Weekly(theRange, region)

				writeToCSV(j, file, df)
				time.sleep(random.randint(0, j))

			j = j + 1

	def viral50Daily(self, output_file, start=None, end=None, region=None):
		"""Write to file the charts data for viral 50 daily
		output_file - CSV file to write the data to
		start - Start of range (YYYY-MM-DD) as string
		end - End of range (YYYY-MM-DD) as string
		region - Region to get data for

		* Any parameter passed as None, means ALL data since the beginning up to now
		"""
		file = validateFile(output_file)
		data = returnDatesAndRegions(start, end, region, isWeekly=False, isViral=True)

		dates = data['dates']
		regions = data['region']

		j = 0
		while(j < len(dates)):
			theRange = dates[j]

			for region in regions:
				self.logger.info('Extracting viral 50 daily for {} - {}'.format(theRange, region))
				df = super().getViral50Daily(theRange, region)

				writeToCSV(j, file, df)
				time.sleep(random.randint(0, j))

			j = j + 1


		






