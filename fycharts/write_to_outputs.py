import pandas as pd
import requests

from .log_config import logger


def writeToCSV(j, output_file, df):
	if(j == 0):
		isHeaders = True
	else:
		isHeaders = False

	try:
		with open(output_file, 'a', encoding="utf-8") as out:
			logger.info(f"Appending data to the file {output_file}...")
			df.to_csv(out, index = False, header = isHeaders, encoding = "utf-8")
			logger.info(f"Done appending to the file {output_file}!!!")
	except Exception as e:
		raise(e)


def writeToSQLTable(which_data, connector, df):
	""" Writes data to an SQL table depending on what data the user is getting
	"""
	if(which_data == "top200Daily"):
		table = "top_200_daily"
	elif(which_data == "top200Weekly"):
		table = "top_200_weekly"
	elif(which_data == "viral50Daily"):
		table = "viral_50_daily"
	elif(which_data == "viral50Weekly"):
		table = "viral_50_weekly"

	try:
		logger.info(f"Appending data to the table {table}")
		df.to_sql(table, con = connector, if_exists = "append")
		logger.info(f"Done appending to the table {table}!!!")
	except Exception as e:
		raise(e)



def postToRestEndpoint(df, urls, which):
	""" Convert df to json, then post to endpoint
	"""
	fd = df.to_dict(orient = "records")
	dump = {"chart": which, "data": fd}

	if(type(urls) is list):
		urls_ = urls
	else:
		urls_ = []
		urls_.append(urls)

	try:
		for url in urls_:
			logger.info(f"POSTing data to the endpoint {url}")
			requests.post(url, json = dump)
			logger.info("Done POSTing")
	except Exception as e:
		raise(e)


# def pushToCallback(df, callback, which):
# 	fd = df.to_dict(orient = "records")
# 	dump = {"chart": which, "data": fd}

# 	try:
# 		logger.info(f"Pushing data to callback function")
# 		callback(dump)
# 		logger.info("Done pusing")
# 	except Exception as e:
# 		raise(e)