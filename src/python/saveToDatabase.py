import gspread
import authGoogleAccount
from gspread import Worksheet


def save_to_database(video_file: str, video_url: str, summary: str) -> None:
    sheet: Worksheet = authGoogleAccount.open_sheet("19pYdNcxu1zWogl_TZukCFEv5HguKBkD_0IT1aRldRPs")

    values_list = sheet.col_values(1)
    empty_row = len(values_list) + 1

    sheet.update('A' + str(empty_row), video_file)
    sheet.update('B' + str(empty_row), video_url)
    sheet.update('C' + str(empty_row), summary)

    print(f"{video_file} has been saved with the summary: {summary}")
