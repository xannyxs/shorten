import os

import toml
import gspread
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from gspread import Client, Spreadsheet, Worksheet
from typing import Any, Optional

config = toml.load("config.shorten.toml")
file_locations_credentials: str = config["file_locations"]["credentials"]


def login_drive() -> Optional[Any]:
    creds = Credentials.from_service_account_file(file_locations_credentials)
    return discovery.build('drive', 'v3', credentials=creds)


# Hardcoded path to credentials.json
def login_gspread() -> Client:
    return gspread.service_account(file_locations_credentials)


def upload_to_drive(video_name: str, video_path: str):
    """
    Uploads a video to Google Drive.

    Args:
        video_name: The name of the video.
        video_path: The path to the video file.

    Returns:
        None
    """
    try:
        drive_service = login_drive()

        file_metadata = {
            'name': video_name,
            'parents': [os.getenv("SHARED_DRIVE_ID")]
        }

        media = MediaFileUpload(video_path)

        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            supportsAllDrives=True,
            fields='id'
        ).execute()

        print('File ID: %s' % file.get('id'))
    except Exception as e:
        print(f"Failed to upload file: {e}")


def open_sheet(spread_id: str) -> Worksheet:
    gc: Client = login_gspread()
    sheet: Spreadsheet = gc.open_by_key(spread_id)
    return sheet.sheet1
