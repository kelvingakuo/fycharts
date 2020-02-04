# fycharts
A fully-fledged installable python package for extracting **top 200** and **viral 50** charts off of [spotifycharts.com](http://spotifycharts.com)

In a nutshell, the unofficial Spotify Charts API

## CONTENTS
1. [Installation](#in)
2. [Sample](#sample)
3. [Functions for data extraction and the parameters they accept](#funcs)
4. [Format for data returned](#format)
5. [Supported country codes](#codes)
6. [A note about dates](#dates)
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
api.top200Daily(output_file = "top_200_daily.csv")
```

Or you want viral 50 daily charts for January 2019 in the us and globally, to be written into a csv file and a SQLLite db *Note: This works only for fycharts>=3.0.0*
```python
myCrawler.py

from fycharts.SpotifyCharts import SpotifyCharts
import sqlalchemy

api = SpotifyCharts()
connector = sqlalchemy.create_engine("sqlite:///spotifycharts.db", echo=False)
api.viral50Daily(output_file = "viral_50_daily.csv", output_db = connector, webhook = "https://mywebhookssite.com/post/", start = "2019-01-01", end = "2019-01-31", region = ["us", "global"])
```

Run your program. 
```bash
python myCrawler.py
```
Watch the terminal for helpful information.

## FUNCTIONS AND PARAMETERS <a id= "funcs"></a>
For all the charts provided by Spotify, four functions exist:
1. top200Weekly()
2. top200Daily()
3. viral50Weekly()
4. viral50Daily()

All four functions take the following parameters:
#### Ouput options
1. output_file - CSV file to write the data to (Compulsory for fycharts<3.0.0)
2. output_db - A connector object for any database supported by SQLAlchemy (only available in fycharts>=3.0.0)
3. webhook - A http endpoint (or list of endpoints) to POST the extracted data to (only available in fycharts>=3.0.0)

    *Create webhooks for testing here: https://webhook.site/ or here: https://beeceptor.com/*

#### Parameters (Optional)
1. start - Start date of range of interest as string with the format YYYY-MM-DD
2. end - End date of range of interest as string with the format YYYY-MM-DD
3. region - Region (or a list of regions e.g. ["global", "us", "fr"]) of interest, as a country abbreviation code. "global" is also valid

    *Refer to [SUPPORTED COUNTRY CODES SO FAR](#codes) below for supported regions.*

If not specified, data is extracted for all dates, all regions

## DATA RETURNED  <a id= "format"></a>
The data extracted from spotifycharts.com is written to the output with the following fields:
1. Position - The song's position during that week or day
2. Track Name - Name of the song
3. Artist - Name of artist
4. Streams - Number of streams for that week or day. **Only applicable to top 200 charts**
5. date - This varies

    For instance if you set 'start = 2020-01-03' & 'end = 2020-01-15'

    For daily charts -> YYYY-MM-DD e.g 2020-01-03

    For top 200 weekly chart -> week_start_date--week_end_date e.g 2020-01-03--2020-01-10

    For viral 50 weekly chart -> week_start_date--week_start_date e.g 2020-01-03--2020-01-03

6. region - Region of the chart as a code

7. spotify_id - Spotify track id ('id' for fycharts < 3.0.0)

**Note:** When writing to a db, fycharts is setup to write:
    1. viral50Daily to the table ```viral_50_daily```
    2. viral50Weekly to the table ```viral_50_weekly```
    3. top200Daily to the table ```top_200_daily```
    4. top200Weekly to the table ```top_200_weekly```

**Note:** To REST endpoints, a JSON payload is sent with the structure:
```bash
{
  "chart": "top_200_daily",
  "data": [
    {
      "Position": 1,
      "Track Name": "The Box",
      "Artist": "Roddy Ricch",
      "Streams": 2278155,
      "date": "2020-01-03",
      "region": "us",
      "spotify_id": "0nbXyq5TXYPCO7pr3N8S4I"
    },
    {
      "Position": 2,
      "Track Name": "Yummy",
      "Artist": "Justin Bieber",
      "Streams": 1863557,
      "date": "2020-01-03",
      "region": "us",
      "spotify_id": "41L3O37CECZt3N7ziG2z7l"
    },
  ]
}
```

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

## ABOUT DATES <a id = "dates"></a>
The start date of the range you"re interested in, is very specific for each chart. If you enter an invalid date, you'll be prompted with a list of suggestions and given a choice whether to use fycharts' suggestion or your own.

*If using multithreading to run multiple functions, the prompt comes up but is non-blocking. You can still respond*

## A RECIPE ON STERIODS  <a id= "turbo"></a>

To fully take advantage of multithreading, you may write your code as follows:

```python
myCrawler.py

import sqlalchemy
import threading

from fycharts.SpotifyCharts import SpotifyCharts

def main():
    api = SpotifyCharts()
    connector = sqlalchemy.create_engine("sqlite:///spotifycharts.db", echo=False)
    hooks = ["https://mywebhookssite.com/post/", "http://asecondsite.net/post"]

    a_thread = threading.Thread(target = api.top200Daily, kwargs = {"output_file": "top_200_daily.csv", "output_db": connector, "webhook": hooks, "start": "2020-01-03", "end":"2020-01-12", "region": ["global", "us"]})
    b_thread = threading.Thread(target = api.top200Weekly, kwargs = {"output_file": "top_200_weekly.csv", "output_db": connector, "webhook": hooks, "start": "2020-01-03", "end":"2020-01-12", "region": ["global", "us"]})
    c_thread = threading.Thread(target = api.viral50Daily, kwargs = {"output_file": "viral_50_daily.csv", "output_db": connector, "webhook": hooks, "start": "2020-01-03", "end":"2020-01-12", "region": ["global", "us"]})
    d_thread = threading.Thread(target = api.viral50Weekly, kwargs = {"output_file": "viral_50_weekly.csv", "output_db": connector, "webhook": hooks, "start": "2020-01-02", "end":"2020-01-12", "region": ["global", "us"]})
    
    a_thread.start()
    b_thread.start()
    c_thread.start()
    d_thread.start()


if __name__ == "__main__":
    main()
```

**TAKE NOTE:** **DO NOT** SHARE THE OUTPUT DESTINATION ACROSS THE FUNCTIONS i.e. each function should be writing to its own set of outputs

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
*This changelog follows a loose version of semantic versioning*
### 3.1.0 4th Feb 2020
**Added**
* Identifying info to payload POSTed to webhook

### 3.0.0 4th Feb 2020
**Added**
* Accepting a DB connector to write data to db
* Accepting a list of REST endpoints to post data to  

**Fixed**
* A bug in file validation

**Changed**
* The Spotify track id column name from 'id' to 'spotify_id'

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
* Released project named "Spotify-Charts-API"
