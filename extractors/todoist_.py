import sqlite3
import pytz
from dateutil import parser
import todoist

"""
    Description:

    Author: pauliusbaulius
    Date: 23.06.2020
    Modified: 23.06.2020
"""


def parse_daily_stats(database_path, api_key):
    # https://developer.todoist.com/sync/v8/?python#get-productivity-stats
    api = todoist.TodoistAPI(api_key)
    api.sync()
    json_data = api.completed.get_stats()

    with sqlite3.connect(database_path) as cn:
        c = cn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS todoist_daily (
					date TEXT PRIMARY KEY, 
					karma_avg INTEGER NOT NULL,
					tasks_completed INTEGER NOT NULL
					)""")

    # reversed karma_graph_data to match order of days_items!
    for day in [{**x, **y} for x, y in zip(json_data["days_items"], reversed(json_data["karma_graph_data"]))]:
        values = (day["date"], day["karma_avg"], day["total_completed"])
        c.execute("INSERT OR REPLACE INTO todoist_daily VALUES (?, ?, ?)", values)

    cn.commit()


def parse_project_items(database_path, api_key):
    api = todoist.TodoistAPI(api_key)
    api.sync()
    items = api.state["items"]

    # TODO write to log!
    print("todoist api returned items:", len(items))

    with sqlite3.connect(database_path) as cn:
        c = cn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS todoist_projects (
							project_id INTEGER PRIMARY KEY,
							name TEXT NOT NULL,
							is_archived INTEGER,
							is_deleted INTEGER,
							is_favorite INTEGER
							)""")

        c.execute("""CREATE TABLE IF NOT EXISTS todoist_project_items (
					project_id INTEGER,
					task_id INTEGER PRIMARY KEY,
					completed TEXT,
					date_added TEXT NOT NULL,
					date_due TEXT,
					task TEXT,
					recurring INTEGER,
					
					FOREIGN KEY (project_id) REFERENCES todoist_projects(project_id)
					)""")

    # FIXME do a check while iterating to see if task is still in items, otherwise delete. Or leave this? It is
    #  pretty dumb to drop the whole table each update, when there will be more tasks it will be PITA.
    c.execute("DELETE FROM todoist_project_items")

    for x in items:
        due = None if x["due"] is None else parser.parse(x["due"]["date"]).astimezone(pytz.utc).isoformat()
        recurring = 0 if x["due"] is None or x["due"]["is_recurring"] is False else 1

        values = (x["project_id"], x["id"], x["date_completed"], x["date_added"], due, x["content"], recurring)

        c.execute("INSERT OR REPLACE INTO todoist_project_items VALUES (?, ?, ?, ?, ?, ?, ?)", values)

        project = api.projects.get_by_id(x["project_id"])
        values = (project["id"], project["name"], project["is_archived"], project["is_deleted"], project["is_favorite"])

        c.execute("INSERT OR REPLACE INTO todoist_projects VALUES (?, ?, ?, ?, ?)", values)

    cn.commit()
