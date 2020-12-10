import requests
import base64
import sqlite3
import datetime

"""
	Description:
		
		This script gets your last 14 days of coding activity from Wakatime and saves
		it to a database. Needs your Wakatime API key and database location.
		
		It saves data into 5 tables:
		
		wakatime_daily date|total_seconds
		wakatime_projects date|name|total_seconds
		wakatime_machines date|name|total_seconds
		wakatime_languages date|name|total_seconds
		wakatime_editors date|name|total_seconds
		
		All seconds are rounded to integers. I haven't found a nice way to track
		project files, since they are found in heartbeats but without total_seconds.
		So you only get time spent per project, but not per project files. Sorry.
	
		You can see many INSERT OR REPLACE queries, this is done to reduce the amount
		of needed code which would be wasted on checks. Since Wakatime API returns all
		values at once, I don't see problem doing this.
		
		Wakatime API calls: https://wakatime.com/developers
		
	Date: 19.06.2020
	Updated: 23.06.2020
	Author: pauliusbaulius
"""


def parse_wakatime(database_path, api_key):
	# Get all stats from today to 14 days back.
	end = datetime.datetime.today()
	start = end - datetime.timedelta(days=14)
	url = f"https://wakatime.com/api/v1/users/current/summaries?start={start.date()}&end={end.date()}"

	# Header has to contain you API key encoded in base64 and "Basic " prepended to it.
	key_base64 = base64.b64encode(api_key.encode("utf-8"))
	key_base64 = str(key_base64, "utf-8")
	header = {"content-type": "application/json", "Authorization": "Basic " + key_base64}

	# Make a request and save response as json object.
	response = requests.get(url, headers=header)
	response_json = response.json()

	with sqlite3.connect(database_path) as cn:
		c = cn.cursor()

		c.execute("""CREATE TABLE IF NOT EXISTS wakatime_daily (date TEXT PRIMARY KEY, total_seconds INTEGER)""")
		c.execute("""CREATE TABLE IF NOT EXISTS wakatime_projects (
					date TEXT, 
					name TEXT, 
					total_seconds INTEGER, 
					PRIMARY KEY(date, name)
					)""")
		c.execute("""CREATE TABLE IF NOT EXISTS wakatime_machines (
					date TEXT, 
					name TEXT, 
					total_seconds INTEGER, 
					PRIMARY KEY(date, name)
					)""")
		c.execute("""CREATE TABLE IF NOT EXISTS wakatime_languages (
					date TEXT, 
					name TEXT, 
					total_seconds INTEGER, 
					PRIMARY KEY(date, name)
					)""")
		c.execute("""CREATE TABLE IF NOT EXISTS wakatime_editors (
					date TEXT, 
					name TEXT, 
					total_seconds INTEGER, 
					PRIMARY KEY(date, name)
					)""")

		def _extract(dictionary, date) -> list:
			# Extracts name of project, machine, language, editor and seconds spent with/in/on it.
			return [(date, x["name"], int(x["total_seconds"])) for x in dictionary]

		for x in response_json["data"]:
			# Iterate over all data points in response and over all data points in those data points using _extract.
			date = x["range"]["date"]
			total_time =  x["grand_total"]["total_seconds"]
			c.execute("INSERT OR REPLACE INTO wakatime_daily VALUES (?, ?)", (date, int(total_time)))

			projects = _extract(x["projects"], date)
			c.executemany("INSERT OR REPLACE INTO wakatime_projects VALUES (?, ?, ?)", projects)

			machines = _extract(x["machines"], date)
			c.executemany("INSERT OR REPLACE INTO wakatime_machines VALUES (?, ?, ?)", machines)

			languages = _extract(x["languages"], date)
			c.executemany("INSERT OR REPLACE INTO wakatime_languages VALUES (?, ?, ?)", languages)

			editors = _extract(x["editors"], date)
			c.executemany("INSERT OR REPLACE INTO wakatime_editors VALUES (?, ?, ?)", editors)

		cn.commit()

	print("wakatime data has been added to the database!")


