import os
import sqlite3
from telethon import TelegramClient

import utils

"""
    Description:
        Telegram chat extraction using Telethon library. Passively extracts messages from all of your chats
        and stores them in a database. Media files are stored in a specified directory.
        
        You will have to enter your phone number and security code sent afterwards the first time you start
        this script.
        
        To make this work, you need api_id and api_hash from telegram. To get those, register a new app:
        https://core.telegram.org/api/obtaining_api_id
        
        telegram_chats:
          datetime|chat_id|message_id|from_me|sender_id|receiver_id|text|file|gif|photo|sticker|video|video_note|voice|
            
        Database stores relative paths to files! Files are stored in predefined directories to reduce database size.
        
        ! cryptg package speeds up downloads, install with $ pip3 install cryptg

    Author: pauliusbaulius
    Date: 20.06.2020
    Modified: 23.06.2020
"""


async def parse_telegram(api_id, api_hash):
    async with TelegramClient('anon', api_id, api_hash) as client:
        # Go over all chats and archive them.
        async for dialog in client.iter_dialogs():
            # https://docs.telethon.dev/en/latest/modules/client.html?highlight=iter_messages#telethon.client.messages.MessageMethods.iter_messages
            # older: max_id=min_from_db, newer: min_id=max_from_db
            newest, oldest = get_newest_oldest_message_id(dialog.id)

            # Get newest messages, then oldest yet not added to the db messages.
            if newest is not None:
                await parse_chat(client, dialog.id, dialog.name, min_id=newest)
            else:
                await parse_chat(client, dialog.id, dialog.name)

            await parse_chat(client, dialog.id, dialog.name, max_id=oldest)
        client.loop.run_until_complete(parse_telegram(api_id, api_hash))


async def parse_chat(client, chat_id, chat_name, **kwargs):
    """Iterates a single chat and downloads data. Writes metadata and message content to db. Media to path.

    Given a chat_id, iterates through chat history. Metadata is written to database table telegram_chats.
    Media like files, videos, pictures and etc. are written to base path specified in config.json.
    Database gets relative path to those files.

    1. Iterate over all chats that are not archived.
    2. Download all new data until existing message id is found! Check if there are holes?
    3. Download media to specified directories.
    4. Save metadata and message text to database.
    """
    messages_parsed = 0

    with (sqlite3.connect(utils.config()["path_database"])) as cn:
        c = cn.cursor()
        table = """CREATE TABLE IF NOT EXISTS telegram_chats ( 
                   datetime TEXT,
                   chat_id INTEGER,
                   message_id INTEGER,
                   from_me INTEGER,
                   sender_id INTEGER,
                   receiver_id INTEGER,
                   text TEXT,
                   file TEXT,
                   gif TEXT,
                   photo TEXT,
                   sticker TEXT,
                   video TEXT,
                   video_note TEXT,
                   voice TEXT,
                   PRIMARY KEY(chat_id, message_id))
                """
        c.execute(table)

        async for message in client.iter_messages(chat_id, **kwargs):
            path = None
            type = None

            if message.photo:
                type = "photo"
            elif message.gif:
                type = "gif"
            elif message.sticker:
                type = "sticker"
            elif message.video:
                type = "video"
            elif message.video_note:
                type = "video_note"
            elif message.voice:
                type = "voice"
            elif message.document:
                type = "file"
            elif message.file:
                type = "file"

            # Group chats have no to_id, use chat_id instead!
            try:
                receiver_id = message.to_id.user_id
            except AttributeError:
                receiver_id = chat_id

            # If it is a text message, download function will raise exception. Use message.text then!
            try:
                path = await download_file(message, type)
                values = (message.date.isoformat(), chat_id, message.id, message.out, message.from_id,
                          receiver_id, message.text, path)
                insert_statement = f"""INSERT OR IGNORE INTO telegram_chats
                                                (datetime, chat_id, message_id, from_me, sender_id, receiver_id, text, {type})
                                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            except AttributeError:
                values = (message.date.isoformat(), chat_id, message.id, message.out, message.from_id,
                          receiver_id, message.text)
                insert_statement = """INSERT OR IGNORE INTO telegram_chats
                                        (datetime, chat_id, message_id, from_me, sender_id, receiver_id, text)
                                        VALUES (?, ?, ?, ?, ?, ?, ?)"""

            c.execute(insert_statement, values)
            cn.commit()
            messages_parsed += 1

    print(f"{chat_name}: added {messages_parsed} messages to the database!")


async def download_file(message, type="") -> str:
    """Downloads media file of telegram message. Stores in preconfigured path from config.json. Skips duplicates."""
    # FIXME handle sticker name, since all are just AnimatedSticker.tps or some shit like that?!
    base_path = os.path.join(utils.config()["path_media"], "telegram")
    # Filename is either existing filename or internal file id + file extension.
    filename = message.file.id + message.file.ext if message.file.name is None else message.file.name
    path = os.path.join(base_path, type, filename)
    # Skip if exists!
    return path if os.path.exists(path) else await message.download_media(path)


def get_newest_oldest_message_id(chat_id) -> tuple:
    """Returns newest and oldest message id's for given chat id from the database."""
    with (sqlite3.connect(utils.config()["path_database"])) as cn:
        c = cn.cursor()
        c.execute("SELECT MAX(message_id) FROM telegram_chats WHERE chat_id == ?", (chat_id, ))
        max_id = c.fetchone()[0]
        c.execute("SELECT MIN(message_id) FROM telegram_chats WHERE chat_id == ?", (chat_id, ))
        min_id = c.fetchone()[0]
        return max_id, min_id