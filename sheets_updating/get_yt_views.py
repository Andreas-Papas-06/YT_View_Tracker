import pandas as pd
import sqlite3 
import os
import sqlite3
from datetime import date
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from googleapiclient.discovery import build
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

def get_views():
    #getting views for each video and adding to db
    conn = sqlite3.connect('view_tracker.db')
    c = conn.cursor()

    c.execute("SELECT * FROM videos_info")
    items = c.fetchall()

    load_dotenv()
    API_KEY = os.getenv("YT_API_KEY")
    youtube = build("youtube", "v3", developerKey=API_KEY)

    def get_video_id(url):
        if "youtu.be" in url:
            return url.split("/")[-1]
        return parse_qs(urlparse(url).query)["v"][0]

    def get_video_views(video_id):
        request = youtube.videos().list(part="statistics", id=video_id)
        response = request.execute()
        if not response["items"]:
            return "Video Not Found"  
        return int(response["items"][0]["statistics"]["viewCount"])

    for item in items:
        try:
            views = get_video_views(get_video_id(item[1]))
        except:
            views = 'Video Not Found'
        row = (date.today().strftime("%Y-%m-%d"), item[0], item[1], views,)
        c.execute("INSERT INTO views VALUES(?,?,?,?)", row)




    #writting to Weekly_Tracker
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
    tab = sheet.worksheet("Weekly_Tracker")
    df = pd.read_sql_query("SELECT * FROM views", conn)
    tab.clear()
    set_with_dataframe(tab, df)


    conn.commit()
    conn.close()


if __name__ == '__main__':
    get_views()