#! /usr/bin/env python3.10
import os
import sys
from os.path import join, dirname, basename, isfile, isdir
from LivePeerSDK_Python.LivePeerSDK import LivePeerSDK
from dotenv import load_dotenv


def upload_video(LivePeer: LivePeerSDK, video_path: str) -> None:
    """Uploads a video to LivePeer."""

    print(f"Uploading... {basename(video_path)}")

    assetUrl = LivePeer.createUploadUrl(basename(video_path))
    LivePeer.uploadContent(video_path, assetUrl['url'])


def main() -> None:
    if len(sys.argv) != 2:
        print(sys.argv)
        print("Usage: python3 upload-video.py /path/to/directory_or_video")
        sys.exit(1)

    videos = get_video()
    if videos:
        LivePeer = LivePeerSDK(os.environ.get("LIVEPEER_API_KEY"))
        upload_video(LivePeer, videos)


if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '../.env.local')
    load_dotenv(dotenv_path)

    main()
