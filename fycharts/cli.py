import click

from fycharts.SpotifyCharts import SpotifyCharts

@click.command()
@click.option("--start", "-s", help = "Start date of chart (YYYY-MM-DD)")
@click.option("--end", "-e", help = "End date of chart (YYYY-MM-DD)")
@click.option("--region", "-r", multiple = True, help = "The region(s) to get the chart for")
@click.option("--csv", "-c", default = '', help = "CSV file to output to")
@click.option("--webhook", "-w", multiple = True, help = "Webhook(s) to POST the data to ")
@click.argument("chart")
def main(chart, start, end, csv, region, webhook):
	""" CLI version of fycharts (https://pypi.org/project/fycharts/)
	
	fycharts [OPTIONS] chartName

	===== EXAMPLES

	fycharts --csv out.csv viral50Weekly
	
	fycharts --start 2020-05-06 --end 2020-10-10 --csv out.csv viral50Weekly
	
	fycharts --region US viral50Weekly
	
	fycharts -r US -r UK viral50Weekly
	
	fycharts --webhook https://mywebhook.site/1232/post viral50Weekly
	
	fycharts -w https://mywebhook.site/1/post -w https://mywebhook.site/2/post viral50Weekly
	
	======
	"""
	region = list(region)
	webhook = list(webhook)

	if(len(region) == 0):
		region = None

	if(len(webhook) == 0 and csv == ''):
		click.secho("ERROR: Please set at least one output mode (CSV or webhooks)", fg = "red", bold = True)
	else:																																		
		api = SpotifyCharts()
		chart_choices = ["top200Weekly", "top200Daily", "viral50Weekly", "viral50Daily"]

		if(chart == "top200Weekly"):
			click.secho("Extracting top200Weekly...", fg = "cyan", bold = True)
			api.top200Weekly(csv, None, webhook, start, end, region)
			click.secho("Extraction complete\n", fg = "white", bold = True)
		elif(chart == "top200Daily"):
			click.secho("Extracting top200Daily...", fg = "cyan", bold = True)
			api.top200Daily(csv, None, webhook, start, end, region)
			click.secho("Extraction complete\n", fg = "white", bold = True)
		elif(chart == "viral50Weekly"):
			click.secho("Extracting viral50Weekly...", fg = "cyan", bold = True)
			api.viral50Weekly(csv, None, webhook, start, end, region)
			click.secho("Extraction complete\n", fg = "white", bold = True)
		elif(chart == "viral50Daily"):
			click.secho("Extracting viral50Daily...", fg = "cyan", bold = True)
			api.viral50Daily(csv, None, webhook, start, end, region)
			click.secho("Extraction complete\n", fg = "white", bold = True)
		else:
			click.secho(f"ERROR: {chart} could not be processed. Select either of: {', '.join(chart_choices)}", fg = "red", bold = True)