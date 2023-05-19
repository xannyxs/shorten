import os
import sys
import tempfile
import saveToDatabase
from LivePeerSDK_Python.LivePeerSDK import LivePeerSDK
from summarizeVideo import start_summary

import time


def process_file(video_file_path: str, assetUrl: any, LivePeer: LivePeerSDK) -> None:
    max_timeout = 600
    sleep_interval = 20
    elapsed_time = 0

    while elapsed_time < max_timeout:
        asset = LivePeer.retrieveAsset(assetUrl['asset']['id'])
        if 'playbackUrl' in asset:
            break
        else:
            print("Waiting for 'playbackUrl' to be available...")
            time.sleep(sleep_interval)
            elapsed_time += sleep_interval

    if 'playbackUrl' not in asset:
        print("Timed out waiting for 'playbackUrl'")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tempdir:
        temp_file_path = os.path.join(tempdir, video_file_path)

        print(f'Summarizing video in {temp_file_path}...')
        start_summary(asset["playbackUrl"], temp_file_path)
        print('Created summary...')

        with open(f'{temp_file_path}.txt') as file:
            summary_content = file.read()

        saveToDatabase.save_to_database(video_file_path, summary_content)