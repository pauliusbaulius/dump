import requests
import datetime
import sqlite3
import pytz

"""
	Description:
		
		This script extracts your last.fm scrobble history.
		In the first run, it will try to get the complete history of your scrobbles.
		In next and following runs, it will only get the new scrobbles.
		
		Data is saved into given database with a following table format:
		    lastfm_scrobbles date|track|artist|album
		    
		! Your scrobbles should be public, otherwise API needs logging in and I have not implemented that !
		
	Date: 23.06.2020
	Updated: 23.06.2020
	Author: pauliusbaulius
"""


def parse_scrobbles(database_path, api_key, username):
    # First response to extract number of pages for iteration.
    url = f"""http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks
              &user={username}
              &api_key={api_key}
              &limit=200
              &format=json
              """
    response = requests.get(url)
    response_json = response.json()

    # Get the amount of pages to iterate.
    pages = response_json['recenttracks']['@attr']['totalPages']

    with sqlite3.connect(database_path) as cn:
        c = cn.cursor()
        # Date is primary key, since you cannot listen to two songs at once, unless you account is stolen.
        c.execute("""CREATE TABLE IF NOT EXISTS lastfm_scrobbles (
                     date TEXT PRIMARY KEY, 
                     track TEXT, 
                     artist TEXT, 
                     album TEXT
                     )""")

        # If there have been no previous entries, set it to None.
        try:
            # Get the newest scrobble from the database.
            c.execute("SELECT date FROM lastfm_scrobbles ORDER BY date DESC LIMIT 1")
            newest_scrobble = c.fetchone()[0]
        except TypeError:
            newest_scrobble = None

        scrobbles = 0

        for page in range(1, int(pages) + 1):
            url = f"""http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks
                      &user={username}
                      &api_key={api_key}
                      &limit=200
                      &page={page}
                      &format=json
                      """
            response = requests.get(url)
            response_json = response.json()["recenttracks"]["track"]

            for track in response_json:

                try:
                    # Convert to UTC.
                    dt = datetime.datetime.fromtimestamp(int(track['date']['uts']))
                    dt = dt.astimezone(pytz.utc)
                    dt = dt.isoformat()
                # Ignore now playing, will add it as past song next time this script runs.
                except KeyError:
                    continue

                values = (dt, track['name'], track['artist']['#text'], track['album']['#text'])
                c.execute("INSERT OR IGNORE INTO lastfm_scrobbles VALUES (?, ?, ?, ?)", values)

                if newest_scrobble is not None and newest_scrobble == dt:
                    cn.commit()
                    print(f"added {scrobbles} new scrobbles to the database!")
                    return

                scrobbles += 1

            cn.commit()
        print(f"added {scrobbles} new scrobbles to the database!")
