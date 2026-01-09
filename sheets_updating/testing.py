import pandas as pd
import sqlite3 


conn = sqlite3.connect('view_tracker.db')
c = conn.cursor()

c.execute("SELECT * FROM videos_info")

items = c.fetchall()
for item in items:
    print(item)
print("====================================================================")
c.execute("DELETE FROM views")
conn.commit()

c.execute("SELECT * FROM views")

items = c.fetchall()
for item in items:
    print(item)

conn.commit()
conn.close()