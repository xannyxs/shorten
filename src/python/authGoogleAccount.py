import gspread
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from gspread import Client, Spreadsheet, Worksheet
from typing import Any, Optional

# def login_drive() -> Optional[Any]:
# creds = Credentials.from_service_account_file("credentials.json")
# return discovery.build('drive', 'v3', credentials=creds)


# Hardcoded path to credentials.json
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
