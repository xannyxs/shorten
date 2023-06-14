import os
import toml
import authGoogleAccount
from gspread import Worksheet

config = toml.load("config.shorten.toml")
database_type: str = config["database"]["type"]

if database_type == "GDrive":
    SHEETID = os.getenv('SHEET_ID')
    if not SHEETID:
        raise EnvironmentError("SHEET_ID environment variable not set")
else:
    raise EnvironmentError("Missing database type. The following options are available:\n\n 1. GDrive")

save_video: str = config["video"]["save_video"]


# Be aware it now pastes the text in the first 3 empty cells
def save_to_gdrive(video_path: str, video_url: str, summary: str) -> None:
    sheet: Worksheet = authGoogleAccount.open_sheet(SHEETID)

    values_list = sheet.col_values(1)
    empty_row = len(values_list) + 1

    sheet.update('A' + str(empty_row), video_path)
    sheet.update('D' + str(empty_row), video_url)
    sheet.update('E' + str(empty_row), summary)

    print(f"{video_path} has been saved with the summary: {summary}")


def save_to_database(video_path: str, video_url: str, summary: str) -> None:
    if database_type == "GDrive":
        save_to_gdrive(video_path, video_url, summary)

    if save_video is True:
        authGoogleAccount.upload_to_drive(os.path.basename(video_path), video_path)
