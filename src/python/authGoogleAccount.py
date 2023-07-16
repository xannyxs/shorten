import gspread
import os
import json
from gspread import Client, Spreadsheet, Worksheet


def login_gspread() -> Client:
    json_credentials = os.getenv('GCP_CREDENTIALS')

    if json_credentials is None:
        print('Environment variable not found')
    else:
        credentials = json.loads(json_credentials)

    return gspread.service_account_from_dict(credentials)


def open_sheet(spread_id: str) -> Worksheet:
    gc: Client = login_gspread()
    sheet: Spreadsheet = gc.open_by_key(spread_id)
    return sheet.sheet1
