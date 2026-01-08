import sqlite3


conn = sqlite3.connect('video.db')

c = conn.cursor()



conn.commit()

conn.close()