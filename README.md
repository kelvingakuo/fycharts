# fycharts
A fully-fledged installable python package for extracting **top 200** and **viral 50** charts off of [spotifycharts.com](http://spotifycharts.com)

In a nutshell, the unofficial Spotify Charts API

## INSPIRATION
This was built to fill the gap left when Spotify deprecated their official Spotify charts API. It arose as a needed crawler for the Spotify data analysis and machine learning project done [here](https://kelvingakuo.github.io)

## INSTALLATION
```bash
pip install fycharts
```

## SAMPLE USAGE
Say you want to extract top 200 daily charts for all time, all regions
```python
myCrawler.py


from fycharts import SpotifyCharts 

api = SpotifyCharts.SpotifyCharts()
api.top200Daily(output_file = 'top_200_daily.csv')
```
Run your program. 
```bash
python myCrawler.py
```
Watch the terminal for helpful information.

## FUNCTIONS AND PARAMETERS
Four functions, for all data you need are required:
1. top200Weekly
2. top200Daily
3. viral50Weekly
4. viral50Daily

All four functions take the following parameters:
#### Compulsory
1. output_file - CSV file to dump the data. 

#### Optional
1. start - Start date of range of interest as string YYYY-MM-DD
2. end - End date of range of interest as string YYYY-MM-DD
3. region - Region of interest, as a country abbreviation code. 'global' is also valid

**Refer to 'SUPPORTED COUNTRY CODES SO FAR' below for important information of this.**

If not included, data is extracted for all dates, all regions

## DATA RETURNED
The data extracted from spotifycharts.com is written into a CSV file with the following fields:
1. position - The song's position during that week or day
2. track name - Name of the song
3. artist - Name of artist
4. region - Region of the chart as a code
5. date - Date or range of dates of chart
6. id - Spotify track id
7. streams - Number of streams for that week or day. **Only applicable to top 200 charts**

## SUPPORTED COUNTRY CODES SO FAR
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

## PASSING DATES AS PARAMETERS
If the date isn't valid, you shall be notified with a list of the closest dates to what you put in, as suggestions.


## STUFF YOU SHOULD KNOW
When extracting data for a range of dates, in loop, the crawler sleeps every iteration for a random number of seconds between 0 and the index of the date. Dig into the code to change this!!!

