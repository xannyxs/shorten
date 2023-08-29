import sys
import json
from tempfile import TemporaryDirectory
import os

from os.path import basename
# from summarizeVideo import start_summary

# BASE_URL = 'https://livepeer.com/api'
# API_KEY = os.getenv('LIVEPEER_API_KEY')
# if not API_KEY:
#     raise EnvironmentError("LIVEPEER_API_KEY environment variable not set")


def process_file(playbackUrl: str) -> str:
    with TemporaryDirectory() as tempdir:
        temp_file_path = os.path.join(tempdir, basename(playbackUrl))

        print(f'Summarizing video in {temp_file_path}...')
        # start_summary(playbackUrl, temp_file_path)
        # print('Created summary...')

        with open(f'{temp_file_path}.txt') as file:
            summary_content = file.read()

        return summary_content


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("Usage: python3 transcodeVideo.py JsonFile")

    print("First arg: ", sys.argv[1])

    file_batch = json.loads(sys.argv[1])
    for file in file_batch:
        with open(file, 'r') as json_file:
            data = json.load(json_file)

        if 'videoUrl' in data and 'name' in data:
            description = process_file(data['videoUrl'])
            data['gpt_description'] = description

            with open(sys.argv[2], 'w') as json_file:
                json.dump(data, json_file, indent=4)
