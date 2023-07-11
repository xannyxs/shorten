import sys
import tempfile
from os.path import basename
from typing import List, Any

import saveToDatabase
import os
import requests
from summarizeVideo import start_summary
from utils import eprint

BASE_URL = 'https://livepeer.com/api'
API_KEY = os.getenv('LIVEPEER_API_KEY')
if not API_KEY:
    raise EnvironmentError("CHATGPT_API_KEY environment variable not set")


def getAssets() -> List[Any]:
    headers = {
        'Authorization': f'Bearer {API_KEY}',
    }

    nextPage = ''
    assets: List[Any] = []

    while len(assets) < 50:
        response = requests.get(f'{BASE_URL}/asset?limit=100&cursor={nextPage}', headers=headers)
        items: Any = response.json()
        for asset in items:
            if len(assets) == 50:
                break
            assets.append(asset)

        if items == '' or len(assets) == 50:
            break

        nextPage = items

    print(f'Fetched {len(assets)} assets')
    return assets


def getEventVideos(assets: List[Any]) -> List[Any]:
    eventAssets = []

    for asset in assets:
        if asset['name'].startswith('FtC'):
            eventAssets.append(asset)

    return eventAssets


def process_file(videoName: str, playbackUrl: str) -> None:
    with tempfile.TemporaryDirectory() as tempdir:
        temp_file_path = os.path.join(tempdir, basename(playbackUrl))

        print(f'Summarizing video in {temp_file_path}...')
        start_summary(playbackUrl, temp_file_path)
        print('Created summary...')

        with open(f'{temp_file_path}.txt') as file:
            summary_content = file.read()

        saveToDatabase.save_to_database(videoName, summary_content)


if __name__ == '__main__':
    if len(sys.argv) != 1:
        eprint("Usage: python script.py")
        sys.exit(1)

    assets = getAssets()
    eventAssets = getEventVideos(assets)
    print('Got assets of event')

    for asset in eventAssets:
        videoName = asset['name'].replace('FtC-session-', '').replace('-', ' ')
        process_file(videoName, asset['playbackUrl'])
