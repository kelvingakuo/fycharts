# fycharts
A fully-fledged installable python package for extracting **top 200** and **viral 50** charts off of [spotifycharts.com](http://spotifycharts.com)

In a nutshell, the unofficial Spotify Charts API

## CONTENTS
1. [Installation](#in)
2. [Sample](#sample)
3. [Functions for data extraction and the parameters they accept](#funcs)
4. [Format for data returned](#format)
5. [Supported country codes](#codes)
6. [Turbo-boosted recipe](#turbo)
7. [Utilities you may find useful](#utils)
8. [Changelog](#change)

## INSPIRATION
This was built to fill the gap left when Spotify deprecated their official Spotify charts API. It arose as a needed crawler for the Spotify data analysis and machine learning project done [here](https://kelvingakuo.github.io)

## INSTALLATION <a id="in"></a>
```bash
pip install fycharts
```
## SAMPLE USAGE <a id="sample"></a>
Say you want to extract top 200 daily charts for all time, all regions
```python
myCrawler.py

from fycharts.SpotifyCharts import SpotifyCharts

api = SpotifyCharts()
api.top200Daily(output_file = 'top_200_daily.csv')
```
Run your program. 
```bash
python myCrawler.py
```
Watch the terminal for helpful information.

## FUNCTIONS AND PARAMETERS <a id= "funcs"></a>
For all the charts provided by Spotify, four functions exist:
1. top200Weekly
2. top200Daily
3. viral50Weekly
4. viral50Daily

All four functions take the following parameters:
#### Compulsory
1. output_file - CSV file to dump the data. 

*For V3.0.0 more outputs e.g. SQL db, REST endpoint etc. will be available. Stay tuned*

#### Optional
1. start - Start date of range of interest as string with the format YYYY-MM-DD
2. end - End date of range of interest as string with the format YYYY-MM-DD
3. region - Region of interest, as a country abbreviation code. 'global' is also valid

    **region can also be a list of regions e.g. ["global", "us", "fr"]**

    **Refer to [SUPPORTED COUNTRY CODES SO FAR](#codes) below for accepted regions.**

If not included, data is extracted for all dates, all regions

## DATA RETURNED  <a id= "format"></a>
The data extracted from spotifycharts.com is written to the output (usually a CSV file) with the following fields:
1. position - The song's position during that week or day
2. track name - Name of the song
3. artist - Name of artist
4. region - Region of the chart as a code
5. date - Date or range of dates of chart
6. spotify_id - Spotify track id
7. streams - Number of streams for that week or day. **Only applicable to top 200 charts**

## SUPPORTED COUNTRY CODES SO FAR  <a id= "codes"></a>
|   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|
|ad |ca |dk |gr |is |mx |ph |sv |
|ar |ch |do |gt |it |my |pl |th |
|at |cl |ec |hk |jp |ni |pt |tr |
|au |co |ee |hn |lt |nl |py |tw |
|be |cr |es |hu |lu |no |ro |us |
|bg |cy |fi |id |lv |nz |se |uy |
|bo |cz |fr |ie |mc |pa |sg |vn |
|br |de |gb |il |mt |pe |sk |global|

## A RECIPE ON STERIODS  <a id= "turbo"></a>

To fully take advantage of multithreading, you may write your code as follows:

```python
myCrawler.py


import threading

from fycharts.SpotifyCharts import SpotifyCharts

def main():
    api = SpotifyCharts()

    a_thread = threading.Thread(target = api.top200Daily, args = ("top_200_daily.csv",), kwargs = {"start": "2020-01-03", "end":"2020-01-12", "region": ["global", "us"]})
    b_thread = threading.Thread(target = api.top200Weekly, args = ("top_200_weekly.csv",), kwargs = {"start": "2020-01-03", "end":"2020-01-12", "region": ["global", "us"]})
    c_thread = threading.Thread(target = api.viral50Daily, args = ("viral_50_daily.csv",), kwargs = {"start": "2020-01-03", "end":"2020-01-12", "region": ["global", "us"]})
    d_thread = threading.Thread(target = api.viral50Weekly, args = ("viral_50_weekly.csv",), kwargs = {"start": "2020-01-02", "end":"2020-01-12", "region": ["global", "us"]})
    
    a_thread.start()
    b_thread.start()
    c_thread.start()
    d_thread.start()


if __name__ == "__main__":
    main()
```

**TAKE NOTE:** DO NOT SHARE THE OUTPUT DESTINATION ACROSS THE FUNCTIONS i.e. each function should be writing to its own set of outputs

## UTILITY FUNCTIONS <a id = "utils"></a>
This library exposes some functions that you may find of use:

1. validDates(start, end, desired)

This function prints a list of valid dates for the kind of data you are interested in.

#### Parameters
1. start - Start date of range of interest as string with the format YYYY-MM-DD
2. end - End date of range of interest as string with the format YYYY-MM-DD
3. desired - A string specifying the kind of data desired

        Accepts:
            * top200Daily
            * top200Weekly
            * viral50Daily
            * viral50Weekly






## CHANGELOG <a id = "change"></a>
### 2.0.1 31st Jan 2020
**Fixed**
* A bug in setting the column titles when multiple regions are requested
### 2.0.0 30th Jan 2020
**Added**
* Multithreading to increase crawling speeds
* Custom exceptions
* A utility method to print valid dates
* Accepting a list of regions

**Improved**
* The documentation
### 1.2.0 5th April 2019
* Improved date verification
### 1.0.1 5th Jan 2019
* Renamed the project to fycharts
### 1.0.0 26th Dec 2018
* Released project named 'Spotify-Charts-API'
