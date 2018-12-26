import requests
from requests import get
import datetime
import json
import sys
import pandas as pd
import csv
import os
import re
import logging
import random
import time
import itertools


logging.basicConfig(filename='logs.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

def returnDates(end, isWeekly, isViral): #Generate range of dates 
	end = datetime.datetime.strptime(end, "%Y-%m-%d")
	ls = [] 
	if(isWeekly): #200: 2016-12-22  Viral:2017-01-05
		if(isViral):
			start = datetime.datetime.strptime("2017-01-05", "%Y-%m-%d")
			gen = [start + datetime.timedelta(weeks=x) for x in range(0, (end-start).days+1)]
			for date in gen:
				if(date<end):
					dt = date + datetime.timedelta(days=0)
					ls.append(dt.strftime("%Y-%m-%d"))
		else:
			start = datetime.datetime.strptime("2016-12-22", "%Y-%m-%d") 
			gen = [start + datetime.timedelta(weeks=x) for x in range(0, (end-start).days+1)]
			for date in gen:
				if(date<end):
					dt = date + datetime.timedelta(days=1)
					ls.append(dt.strftime("%Y-%m-%d"))

	else:
		start = datetime.datetime.strptime("2017-01-01", "%Y-%m-%d") #Daily: 2017-01-01
		gen = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
		for date in gen:
			if(date<=end):
				ls.append(date.strftime("%Y-%m-%d"))

	return ls

def regex(url):
	if(type(url) == str):
		sr = re.search(r'https://open.spotify.com/track/(.*)' ,url, re.I|re.M)
		trackId = sr.group(1)
	else:
		trackId = 'N/A'
	
	return trackId

def cleanUp(data, date, region, isSkip):
	fl = open('tempFile.csv', 'wb')
	fl.write(data)
	fl.close()

	if(isSkip):
		df = pd.read_csv('tempFile.csv', skiprows=1)
	else:
		df = pd.read_csv('tempFile.csv')

	os.remove('tempFile.csv')

	df['date'] = date
	df['region'] = region
	df['id'] =  df['URL'].apply(lambda x: regex(x))
	df.drop(['URL'], axis=1, inplace=True)

	return df

def writeData(url, date, region, outFile, isSkip, nas, isViral):
	headers = {'Host':'spotifycharts.com', 
				'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'}
	now = url
	try:
		res = get(url, headers =headers)
	except requests.exceptions.RequestException as e:
		logging.debug('_________----------_________---------SOME PROBLEM OCCURED HERE_________----------_________---------')
		logging.debug(e)
		time.sleep(random.randint(0,3600))
		res = get(now, headers =headers)

	if(res.status_code == 200):
		if(res.headers['Content-Type'] == 'text/html; charset=UTF-8'): #Data does not exist
			pos = list(itertools.repeat("NA", nas))
			track = list(itertools.repeat("NA", nas))
			art = list(itertools.repeat("NA", nas))
			stre = list(itertools.repeat("NA", nas))
			reg = list(itertools.repeat(region, nas))
			dat = list(itertools.repeat(date, nas))
			i = list(itertools.repeat("NA", nas))

			if(isViral):
				appe = pd.DataFrame.from_dict({'position': pos, 'track name':track, 'artist':art, 'region': reg, 'date':dat, 'id':i})
			else:
				appe = pd.DataFrame.from_dict({'position': pos, 'track name':track, 'artist':art, 'streams':stre, 'region': reg, 'date':dat, 'id':i})

		else:
			tings = res.content
			if(isSkip):
				appe = cleanUp(tings, date, region, True)
			else:
				appe = cleanUp(tings, date, region, False)

	else:
		logging.debug('_________----------SERVER ERROR OR STH_________---------')
		pos = list(itertools.repeat("NA", nas))
		track = list(itertools.repeat("NA", nas))
		art = list(itertools.repeat("NA", nas))
		stre = list(itertools.repeat("NA", nas))
		reg = list(itertools.repeat(region, nas))
		dat = list(itertools.repeat(date, nas))
		i = list(itertools.repeat("NA", nas))

		appe = pd.DataFrame.from_dict({'position': pos, 'track name':track, 'artist':art, 'streams':stre, 'region': reg, 'date':dat, 'id':i})


	with open('data/'+outFile, 'a') as fl:
		appe.to_csv(fl, index=False, header=False)
	

def createFile(name, subdir, isViral):
	f = open('data/'+subdir+'/'+name, 'wb')
	wr = csv.writer(f, delimiter=',')
	if(isViral):
		wr.writerow(['position','track name', 'artist', 'date', 'region', 'id'])
	else:
		wr.writerow(['position','track name', 'artist', 'streams', 'date', 'region', 'id'])
	f.close()



def top200Weekly(dates, regions):
	i = 0
	ln = len(dates)
	while i < ln:
		rang = dates[i]+'--'+dates[i+1]
		logging.debug(rang)
		i = i + 1
		time.sleep(random.randint(0,10))

		subdir = 'top200Weekly'
		fil = rang + '.csv'
		createFile(fil, subdir, False)

		into = subdir+'/'+fil


		for region in regions:
			url = 'https://spotifycharts.com/regional/{}/weekly/{}/download'.format(region, rang)
			writeData(url, rang, region, into, True, 200, False)
			time.sleep(random.randint(0,10))


def viral50Weekly(dates, regions):
	i = 0
	ln = len(dates)
	while i < ln:
		rang = dates[i]+'--'+dates[i]
		logging.debug(rang)
		i = i + 1
		time.sleep(random.randint(0,10))

		subdir = 'viral50Weekly'
		fil = rang + '.csv'
		createFile(fil, subdir, True)

		into = subdir+'/'+fil


		for region in regions:
			url = 'https://spotifycharts.com/viral/{}/weekly/{}/download'.format(region, rang)
			writeData(url, rang, region, into, False, 50, True)
			time.sleep(random.randint(0,20))


def viral50Daily(dates, regions):
	subdir = 'viral50Daily'
	fil = 'viral50Daily'+'.csv'
	createFile(fil, subdir, True)

	into = subdir+'/'+fil
	

	for date in dates:
		logging.debug(date)
		time.sleep(random.randint(0,30))

		for region in regions:
			url = 'https://spotifycharts.com/viral/{}/daily/{}/download'.format(region, date)
			writeData(url, date, region, into, False, 50, True)
			time.sleep(random.randint(0,30))

def top200Daily(dates, regions):
	subdir = 'top200Daily'
	#fil = 'top200Daily'+'.csv'
	#createFile(fil, subdir, False)

	#into = subdir+'/'+fil
	into = subdir+'/'+'top200Daily_pt.csv'
	for date in dates:
		logging.debug(date)

		for region in regions:
			url = 'https://spotifycharts.com/regional/{}/daily/{}/download'.format(region, date)
			writeData(url, date, region, into, True, 200, False)
			time.sleep(random.randint(0,30))

	return 0


def main(end): #Upto 2018-09-30
	regions = ['global', 'ad', 'ar', 'at', 'au', 'be', 'bg', 'bo', 'br', 'ca', 'ch', 'cl', 'co', 'cr', 'cy', 'cz', 'de', 'dk', 'do', 'ec', 'ee', 'es', 'fi', 'fr', 'gb', 'gr', 'gt', 'hk', 'hn', 'hu', 'id', 'ie', 'il', 'is', 'it', 'jp', 'lt', 'lu', 'lv', 'mc', 'mt', 'mx','my', 'ni', 'nl', 'no', 'nz', 'pa', 'pe', 'ph', 'pl', 'pt', 'py', 'ro', 'se', 'sg', 'sk', 'sv', 'th', 'tr', 'tw', 'us', 'uy', 'vn'] #Verify existence of link first. Some have viral 50 but no top 200

	wks200 = returnDates(end,True, False)
	wks50 = returnDates(end, True, True)
	dys = returnDates(end, False, False)

	#Cleaning: Some columns are 'N/A'
	#Change: Weekly code to dump into one CSV

	#top200Weekly(wks200, regions)
	#viral50Weekly(wks50, regions)
	#viral50Daily(dys, regions)
	top200Daily(dys, regions)

	


if __name__ == "__main__":
	main(sys.argv[1])
#argv[1]: End date in YYYY-MM-DD 