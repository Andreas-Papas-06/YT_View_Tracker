import sqlite3


conn = sqlite3.connect('view_tracker.db')

c = conn.cursor()

c.execute(""" CREATE TABLE videos_info (
          video_name TEXT,
          video_link TEXT,
          date_added TEXT
          )""")

c.execute(""" CREATE TABLE views (
          date TEXT,
          name TEXT,
          link TEXT,
          views TEXT
          )""")

conn.commit()

conn.close()