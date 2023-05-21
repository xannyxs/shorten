import sys
import tempfile
from os.path import basename

import saveToDatabase
import os
from summarizeVideo import start_summary


def process_file(video_file_path: str, playbackUrl: str) -> None:
    with tempfile.TemporaryDirectory() as tempdir:
        temp_file_path = os.path.join(tempdir, basename(video_file_path))

        print(f'Summarizing video in {temp_file_path}...')
        start_summary(playbackUrl, temp_file_path)
        print('Created summary...')

        with open(f'{temp_file_path}.txt') as file:
            summary_content = file.read()

        saveToDatabase.save_to_database(video_file_path, summary_content)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py video_file_path assetId")
        sys.exit(1)

    process_file(sys.argv[1], sys.argv[2])
