import sys
import json
import tempfile
import os

from os.path import basename
from summarizeVideo import start_summary

BASE_URL = 'https://livepeer.com/api'
API_KEY = os.getenv('LIVEPEER_API_KEY')
if not API_KEY:
    raise EnvironmentError("LIVEPEER_API_KEY environment variable not set")

EVENT = os.getenv('EVENT')
if not EVENT:
    raise EnvironmentError("EVENT environment variable not set")


def process_file(playbackUrl: str) -> str:
    with tempfile.TemporaryDirectory() as tempdir:
        temp_file_path = os.path.join(tempdir, basename(playbackUrl))

        print(f'Summarizing video in {temp_file_path}...')
        start_summary(playbackUrl, temp_file_path)
        print('Created summary...')

        with open(f'{temp_file_path}.txt') as file:
            summary_content = file.read()

        return summary_content


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError("Usage: python3 transcodeVideo.py JsonFile")

    with open(sys.argv[2], 'r') as json_file:
        data = json.load(json_file)

    if 'videoUrl' in data and 'name' in data:
        description = process_file(data['videoUrl'])
        data['gpt_description'] = description

        with open(sys.argv[2], 'w') as json_file:
            json.dump(data, json_file, indent=4)
