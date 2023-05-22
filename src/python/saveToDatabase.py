import gspread
import authGoogleAccount
from gspread import Worksheet
from typing import Union


def save_to_database(video_file: str, summary: str) -> None:
    sheet: Worksheet = authGoogleAccount.open_sheet("19pYdNcxu1zWogl_TZukCFEv5HguKBkD_0IT1aRldRPs")

    # Retrieve all records of the data
    records_data = sheet.get_all_records()

    # Find the first empty row
    empty_row = len(records_data) + 1

    # Write to the first empty row
    sheet.update('A' + str(empty_row), video_file)
    sheet.update('B' + str(empty_row), summary)

    print(f"{video_file} has been saved with the summary: {summary}")
