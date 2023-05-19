import gspread
import authGoogleAccount


# Could make this more advanced.
# 1. Give the user more choice on where to upload it
# 2. Say where it should be saved

def save_to_database(video_file: str, summary: str) -> None:
    sheet = authGoogleAccount.open_sheet("19pYdNcxu1zWogl_TZukCFEv5HguKBkD_0IT1aRldRPs")

    sheet.update('A1', video_file)
    sheet.update('B1', summary)

    print(f"{video_file} has been saved with the summary: {summary}")