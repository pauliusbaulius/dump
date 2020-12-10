# TODO perkelt kazkur, cia nereikia
def create_datetime(date, time, timezone):
	"""Converts given date, time and timezone into UTC timestamp in ISO 8601 format."""
	date = [int(x) for x in date.split("-")]
	time = [int(x) for x in time.split(":")]
	timezone = pytz.timezone(timezone)
	dt = datetime.datetime(date[0], date[1], date[2], time[0], time[1], tzinfo=timezone)
	dt = dt.astimezone(pytz.utc)
	dt = dt.isoformat()
	print(type(dt))
	print(dt)
