import authGoogleAccount
import os
import re

DESCRIPTION_COLUMN = 'P'
NAME_COLUMN = 'D:H'
ID_COLUMN = 'C'


def get_position(letter: str) -> int:
    position = ord(letter.upper()) - ord('A') + 1
    return position


def clean_video_ids(video_ids: list[str]) -> list[str]:
    pattern = r'[:,;"\']'

    return [re.sub(pattern, '', id).lower() for id in video_ids]


def get_name(videoID: str) -> str:
    sheet = authGoogleAccount.open_sheet(str(os.environ['SHEET_ID']))

    video_ids = sheet.col_values(get_position(ID_COLUMN))
    cleaned_video_ids = clean_video_ids(video_ids)
    speakers = sheet.col_values(get_position(NAME_COLUMN))

    return speakers


def is_video_id_valid(videoID: str) -> bool:
    sheet = authGoogleAccount.open_sheet(str(os.environ['SHEET_ID']))

    video_ids = sheet.col_values(get_position(ID_COLUMN))
    cleaned_video_ids = clean_video_ids(video_ids)
    descriptions = sheet.col_values(get_position(DESCRIPTION_COLUMN))

    try:
        row_number = cleaned_video_ids.index(videoID.lower()) + 1
    except ValueError:
        print(f"No row found for video ID {videoID}")
        return False

    if row_number <= len(descriptions) and descriptions[row_number -
                                                        1].strip() != '':
        print(
            f"The description for video ID {videoID} has already been filled.")
        return False

    return True


def save_to_database(videoID: str, summary: str) -> None:
    sheet = authGoogleAccount.open_sheet(str(os.environ['SHEET_ID']))

    video_ids = sheet.col_values(get_position(ID_COLUMN))
    cleaned_video_ids = clean_video_ids(video_ids)

    try:
        row_number = cleaned_video_ids.index(videoID.lower()) + 1
    except ValueError:
        print(f"No row found for video ID {videoID}")
        return

    sheet.update(DESCRIPTION_COLUMN + str(row_number), summary)

    print(f"{videoID} has been saved with the summary: {summary}")
