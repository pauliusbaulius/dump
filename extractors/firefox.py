import os
from dateutil import parser
import shutil
import sqlite3
import tempfile
import pytz

"""
    Description:

    Author: pauliusbaulius
    Date: 23.06.2020
    Modified: 23.06.2020
"""



def extract_firefox_data(firefox_db_path):


    if os.path.exists(firefox_db_path):

        # Create temporary file!
        tmp = tempfile.NamedTemporaryFile(delete=True)
        firefox_db_path = os.path.join(firefox_db_path, "places.sqlite")

        # Copy Firefox database to temporary location.
        shutil.copy2(firefox_db_path, tmp.name)

        with sqlite3.connect(tmp.name) as cn:
            c = cn.cursor()

            # https://developer.mozilla.org/en-US/docs/Mozilla/Tech/Places/Database
            c.execute("""SELECT datetime((visit_date/1000000), 'unixepoch', 'localtime'), url, title
                      FROM moz_places INNER JOIN moz_historyvisits on moz_historyvisits.place_id = moz_places.id
                      ORDER BY visit_date
                      """)
            result = c.fetchall()

            # Convert time to UTC ISO format.
            result = [(parser.parse(x[0]).astimezone(pytz.utc).isoformat(), x[1], x[2]) for x in result]

            with sqlite3.connect("firefox.db") as cn:
                c = cn.cursor()

                # TODO primary key? idk if needed.
                c.execute("""CREATE TABLE IF NOT EXISTS firefox_history (
                                    date TEXT NOT NULL,
                                    url TEXT NOT NULL,
                                    title TEXT
                                    )""")

                c.executemany("INSERT OR IGNORE INTO firefox_history VALUES (?, ?, ?)", result)
                cn.commit()

    else:
        print(f"firefox database {firefox_db_path} does not exist!")
