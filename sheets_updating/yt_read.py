import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    r'C:/Users/andre/YT_View_Tracker/sheets_updating/google-creds.json',
    scopes=SCOPES
)

client = gspread.authorize(creds)

sheet = client.open("YouTube_View_Tracker")
videos_tab = sheet.worksheet("Input_Videos")

rows = videos_tab.get_all_records()
print(rows)