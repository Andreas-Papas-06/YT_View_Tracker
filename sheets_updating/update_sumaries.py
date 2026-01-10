import pandas as pd
import sqlite3 
import os
from datetime import date
from dotenv import load_dotenv
from googleapiclient.discovery import build
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import numpy as np
import json



def update_sum():

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds_dict = json.loads(os.environ["GOOGLE_CREDS_JSON"])

    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=SCOPES
    )

    client = gspread.authorize(creds)
    sheet = client.open("YouTube_View_Tracker")
    tab = sheet.worksheet("Summaries")

    conn = sqlite3.connect('view_tracker.db')
    c = conn.cursor()

    c.execute("SELECT video_name FROM videos_info")
    current_names = c.fetchall()
    if current_names == []:
        tab.resize(rows=1)
        return
    names_list = [x for tup in current_names for x in tup]

    rows = []
    for name in names_list:
        c.execute("SELECT views FROM views WHERE name = ? ORDER BY date DESC LIMIT 52", (name,))
        views = c.fetchall()
        views_list = [x for tup in views for x in tup]
        if 'Video Not Found' in views_list:
            continue
        weeks = len(views_list)
        views_list = [int(x) for x in views_list]
        
        if weeks < 2:

            views_week = 0
            views_month = 0
            views_3month = 0 
            views_6month = 0
            views_year = 0
            since_added = 0

        elif weeks < 4:

            views_week = views_list[0] - views_list[1]
            views_month = views_week
            views_3month = views_week
            views_6month = views_week
            views_year = views_week
            since_added = views_week

        elif weeks < 13:

            views_week = views_list[0] - views_list[1]
            views_month = views_list[0] - views_list[3]
            views_3month = views_month 
            views_6month = views_month
            views_year = views_month
            since_added = views_month

        elif weeks < 26:

            views_week = views_list[0] - views_list[1]
            views_month = views_list[0] - views_list[3]
            views_3month = views_list[0] - views_list[12]
            views_6month = views_3month
            views_year = views_3month
            since_added = views_3month

        elif weeks < 52:
            views_week = views_list[0] - views_list[1]
            views_month = views_list[0] - views_list[3]
            views_3month = views_list[0] - views_list[12]
            views_6month = views_list[0] - views_list[25]
            views_year = views_6month
            since_added = views_6month

        else:
            
            views_week = views_list[0] - views_list[1]
            views_month = views_list[0] - views_list[3]
            views_3month = views_list[0] - views_list[12]
            views_6month = views_list[0] - views_list[25]
            views_year = views_list[0] - views_list[51]
            since_added = views_list[0] - views_list[-1]

        rows.append([name, views_week, views_month, views_3month, views_6month, views_year, since_added])
        

        
    arr = np.array(rows)
    array_rows = arr[:, 1:]
    array_rows = array_rows.astype(int)
    total_sum = array_rows.sum(axis=0)
    total_row = total_sum.tolist()
    total_row.insert(0, 'Total')
    rows.append(total_row)
    


    tab.resize(rows=1)
    tab.append_rows(rows, value_input_option="USER_ENTERED")


if __name__ == '__main__':
    update_sum()
    
