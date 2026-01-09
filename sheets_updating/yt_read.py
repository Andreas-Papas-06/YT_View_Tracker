import gspread
from google.oauth2.service_account import Credentials
import sqlite3
from datetime import date


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    'sheets_updating/google-creds.json',
    scopes=SCOPES
)

client = gspread.authorize(creds)
sheet = client.open("YouTube_View_Tracker")
videos_tab = sheet.worksheet("Input_Videos")
rows = videos_tab.get_all_records()
input_videos = [row['Video Name'] for row in rows]

conn = sqlite3.connect('view_tracker.db')
c = conn.cursor()

c.execute("SELECT video_name FROM videos_info")
current_names = c.fetchall()
names_list = [x for tup in current_names for x in tup]
new_vids = []

#adding new vidoes to db
videos_to_add = []
for row in rows:
    if row['Video Name'] not in names_list:
        new_vids.append(row['Video Name'])
        video = tuple([row['Video Name'], row['Video Link'], date.today().strftime("%Y-%m-%d")])
        videos_to_add.append(video)

c.executemany("INSERT INTO videos_info VALUES(?,?,?)", videos_to_add)

#deleting videos from db
for name in names_list:
    if name not in input_videos:
        c.execute(f"DELETE from videos_info WHERE video_name = ?",(name,))

conn.commit()
conn.close()

tab = sheet.worksheet("Input_Videos")

values = tab.get_all_values()

updates = []

for i, row in enumerate(values[1:], start=2):
    if row[0] in new_vids:
        updates.append({
            "range": f"C{i}:D{i}",
            "values": [['Active', str(date.today())]]
        })

if updates:
    tab.batch_update(updates)


    