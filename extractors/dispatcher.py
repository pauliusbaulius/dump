import asyncio

import utils
from scripts.wakatime import parse_wakatime
from scripts.lastfm import parse_scrobbles
from scripts.todoist_ import parse_daily_stats, parse_project_items
from scripts.telegram import parse_telegram

"""
    Description:
        Dispatcher reads the config file, gets all enabled services, runs corresponding data extraction functions.
        
    Author: pauliusbaulius
    Date: 21.06.2020
    Modified: 23.06.2020
"""

# TODO to python note: pretty_json = json.dumps(response_json, indent=4, sort_keys=True)
# TODO store times in seconds and do str(datetime.timedelta(seconds=666))

services = utils.config()["services"]

database_path = utils.config()["path_database"]

api_key = utils.config()["services"]["wakatime"]["api_key"]
parse_wakatime(database_path, api_key)

api_key = utils.config()["services"]["lastfm"]["api_key"]
username = utils.config()["services"]["lastfm"]["username"]
parse_scrobbles(database_path, api_key, username)

api_key = utils.config()["services"]["todoist"]["api_key"]
parse_daily_stats(database_path, api_key)
parse_project_items(database_path, api_key)

api_id = utils.config()["services"]["telegram"]["api_id"]
api_hash = utils.config()["services"]["telegram"]["api_hash"]
# FIXME RuntimeError: This event loop is already running sys:1:
#  RuntimeWarning: coroutine 'parse_telegram' was never awaited
asyncio.run(parse_telegram(api_id, api_hash))
