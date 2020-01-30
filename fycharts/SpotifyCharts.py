import json
import threading

from queue import Queue

from .crawler_base import SpotifyChartsBase
from .compute_dates import returnDatesAndRegions
from .compute_dates import whatDates
from .log_config import logger
from .write_to_file import writeToCSV

from .exceptions import FyChartsException



def validateFile(fileName):
	if('csv' in fileName):
			file = fileName

			return file
	else:
		raise FyChartsException('ONLY CSV FILES ALLOWED!!!')

	

# Class definition
class SpotifyCharts(SpotifyChartsBase):
	def __init__(self):
		SpotifyChartsBase.__init__(self)
		self.data_queue = Queue()

		# self.thread = threading.Thread(target = self.__write_to_csv_from_queue, args = (self.data_queue,))
		# self.thread.start()

	def __write_to_csv_from_queue(self, data_q):
		""" Reads a dataframe from the queue, then writes to CSV
		"""
		try:
			work = True
			while work:
				data = data_q.get(block = True)
				if data is None:
					work = False
					return
				else:
					df = data["df"]
					j = data["j"]
					file = data["out_file"]

					writeToCSV(j, file, df)
		except Exception as e:
			raise RuntimeError(e)

	def top200Weekly(self, output_file, start=None, end=None, region=None):
		"""Write to file the charts data for top 200 weekly
		Params:
			output_file - CSV file to write the data to
			start - Start of range (YYYY-MM-DD) as string
			end - End of range (YYYY-MM-DD) as string
			region - Region (or a list of regions) to get data for

		* Any parameter passed as None, means ALL data since the beginning up to now
		"""
		file = validateFile(output_file)
		data = returnDatesAndRegions(start, end, region, isWeekly=True, isViral=False)

		dates = data['dates']
		regions = data['region']

		a_thread = threading.Thread(target = self.__write_to_csv_from_queue, args = (self.data_queue,))
		a_thread.start()

		j = 0
		while(j < len(dates)):
			if((j + 1) == len(dates)): 
				break
			theRange = dates[j]+'--'+dates[j+1]

			for region in regions:
				self.logger.info('Extracting top 200 weekly for {} - {}'.format(theRange, region))
				df = super().helperTop200Weekly(theRange, region)

				dict_for_thread = {"df": df, "out_file": file, "j": j}
				self.data_queue.put(dict_for_thread)
			j = j + 1
		self.data_queue.put(None)

	def top200Daily(self, output_file, start=None, end=None, region=None):
		"""Write to file the charts data for top 200 daily
		Params:
			output_file - CSV file to write the data to
			start - Start of range (YYYY-MM-DD) as string
			end - End of range (YYYY-MM-DD) as string
			region - Region (or a list of regions) to get data for

		* Any parameter passed as None, means ALL data since the beginning up to now
		"""
		file = validateFile(output_file)
		data = returnDatesAndRegions(start, end, region, isWeekly=False, isViral=False)

		dates = data['dates']
		regions = data['region']

		b_thread = threading.Thread(target = self.__write_to_csv_from_queue, args = (self.data_queue,))
		b_thread.start()

		j = 0
		while(j < len(dates)):
			theRange = dates[j]

			for region in regions:
				self.logger.info('Extracting top 200 daily for {} - {}'.format(theRange, region))
				df = super().helperTop200Daily(theRange, region)
				dict_for_thread = {"df": df, "out_file": file, "j": j}
				self.data_queue.put(dict_for_thread)

			j = j + 1
		self.data_queue.put(None)

	def viral50Weekly(self, output_file, start=None, end=None, region=None):
		"""Write to file the charts data for viral 50 weekly
		Params:
			output_file - CSV file to write the data to
			start - Start of range (YYYY-MM-DD) as string
			end - End of range (YYYY-MM-DD) as string
			region - Region (or a list of regions) to get data for

		* Any parameter passed as None, means ALL data since the beginning up to now
		"""
		file = validateFile(output_file)
		data = returnDatesAndRegions(start, end, region, isWeekly=True, isViral=True)

		dates = data['dates']
		regions = data['region']

		c_thread = threading.Thread(target = self.__write_to_csv_from_queue, args = (self.data_queue,))
		c_thread.start()

		j = 0
		while(j < len(dates)):
			if((j) == len(dates)): 
				break
			theRange = dates[j]+'--'+dates[j]

			for region in regions:
				self.logger.info('Extracting viral 50 weekly for {} - {}'.format(theRange, region))
				df = super().helperViral50Weekly(theRange, region)

				dict_for_thread = {"df": df, "out_file": file, "j": j}
				self.data_queue.put(dict_for_thread)

			j = j + 1
		self.data_queue.put(None)

	def viral50Daily(self, output_file, start=None, end=None, region=None):
		"""Write to file the charts data for viral 50 daily
		Params:
			output_file - CSV file to write the data to
			start - Start of range (YYYY-MM-DD) as string
			end - End of range (YYYY-MM-DD) as string
			region - Region (or a list of regions) to get data for

		* Any parameter passed as None, means ALL data since the beginning up to now
		"""
		file = validateFile(output_file)
		data = returnDatesAndRegions(start, end, region, isWeekly=False, isViral=True)

		dates = data['dates']
		regions = data['region']

		d_thread = threading.Thread(target = self.__write_to_csv_from_queue, args = (self.data_queue,))
		d_thread.start()

		j = 0
		while(j < len(dates)):
			theRange = dates[j]

			for region in regions:
				self.logger.info('Extracting viral 50 daily for {} - {}'.format(theRange, region))
				df = super().helperViral50Daily(theRange, region)

				dict_for_thread = {"df": df, "out_file": file, "j": j}
				self.data_queue.put(dict_for_thread)

			j = j + 1
		self.data_queue.put(None)

	# ====== UTILITY FUNCTIONS ======
	def validDates(self, start, end, desired):
		""" Returns a table of valid dates from a start date to an end date provided, for the specific data desired
		Params:
			start - Start date of range (YYYY-MM-DD) as string
			end - End date of range (YYYY-MM-DD) as string
			desired - A string specifying the kind of data desired
				Accepts:
					* top200Daily
					* top200Weekly
					* viral50Daily
					* viral50Weekly
		"""
		theDates = whatDates(start, end, desired)
		print(json.dumps(theDates, indent = 4))


		


		






