import os
import sqlite3
import random
import requests
from datetime import datetime

def database_connection():
    return sqlite3.connect("quotes_database.db")

def random_quote(cursor):
    cursor.execute("select max(id) from quotes")
    max_id = cursor.fetchone()[0]
    random_number = random.randint(1,max_id)

    cursor.execute("select quote from quotes where id=? and used=0", (random_number,))
    quote = cursor.fetchone()[0]
    cursor.execute("select person from quotes where id=? and used=0", (random_number,))
    person = cursor.fetchone()[0]

    return quote, person

def used_check(cursor):
    cursor.execute("SELECT 1 FROM quotes WHERE used = 0 LIMIT 1")
    if not cursor.fetchone():
        cursor.execute("UPDATE quotes SET used = 0")


def quote_to_used(quote, cursor):
    cursor.execute("update quotes set used=1 where quote=?", (quote,))

def send_quote(quote, person, webhook_url):
    date = datetime.today().strftime("%d. %m.")

    payload = {"content": f"📺 **{date} - TV show quote:**\n> \"*{quote}*\" - {person}"}
    requests.post(webhook_url, json=payload)

def main():
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    conn = database_connection()
    cursor = conn.cursor()
    used_check(cursor)

    quote, person = random_quote(cursor)
    quote_to_used(quote, cursor)

    send_quote(quote, person, webhook_url)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()