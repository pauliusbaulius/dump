import sqlite3

import requests

"""
aw-watcher-afk_paulius-laptop
aw-watcher-web-firefox
aw-watcher-web-chromium
"""

# response = requests.get("http://localhost:5600/api/0/buckets")
# response_json = response.json()
# print(response_json)

response = requests.get(f"http://localhost:5600/api/0/buckets/aw-watcher-window_paulius-laptop/events")
response_json = response.json()

with sqlite3.connect("wakatime.db") as cn:
    c = cn.cursor()
    # Date is primary key, since you cannot listen to two songs at once, unless you account is stolen.
    c.execute(f"""CREATE TABLE IF NOT EXISTS aw_watcher_afk_paulius_laptop (
                 id INTEGER PRIMARY KEY, 
                 timestamp TEXT NOT NULL, 
                 duration REAL NOT NULL, 
                 application TEXT NOT NULL,
                 title TEXT
                 )""")
    for y in response_json:
        values = (y["id"], y["timestamp"], y["duration"], y["data"]["app"], y["data"]["title"])
        c.execute(f"INSERT OR REPLACE INTO aw_watcher_afk_paulius_laptop VALUES(?, ?, ?, ?, ?)", values)
    cn.commit()

def insert_web(response_json):
    # TODO extract domain before adding, add as domain column
    with sqlite3.connect("wakatime.db") as cn:
        c = cn.cursor()
        # Date is primary key, since you cannot listen to two songs at once, unless you account is stolen.
        c.execute(f"""CREATE TABLE IF NOT EXISTS aw_watcher_web (
                     id INTEGER PRIMARY KEY,
                     timestamp TEXT NOT NULL,
                     duration REAL NOT NULL,
                     url TEXT NOT NULL,
                     title TEXT,
                     audible INTEGER NOT NULL,
                     incognito INTEGER NOT NULL,
                     tab_count INTEGER NOT NULL
                     )""")
        for y in response_json:
            values = (
            y["id"], y["timestamp"], y["duration"], y["data"]["url"], y["data"]["title"], y["data"]["audible"],
            y["data"]["incognito"], y["data"]["tabCount"])
            c.execute(f"INSERT OR REPLACE INTO aw_watcher_web VALUES(?, ?, ?, ?, ?, ?, ?, ?)", values)
        cn.commit()

response = requests.get(f"http://localhost:5600/api/0/buckets/aw-watcher-web-firefox/events")
response_json = response.json()
insert_web(response_json)

response = requests.get(f"http://localhost:5600/api/0/buckets/aw-watcher-web-chromium/events")
response_json = response.json()
insert_web(response_json)

