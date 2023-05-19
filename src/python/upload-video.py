#! /usr/bin/env python3.10
import os
import sys
from os.path import basename
from transcodeVideo import process_file
from LivePeerSDK_Python.LivePeerSDK import LivePeerSDK



def upload_video(LivePeer: LivePeerSDK, video_path: str) -> any:
    """Uploads a video to LivePeer."""

    print(f"Uploading... {basename(video_path)}")

    assetUrl = LivePeer.createUploadUrl(basename(video_path))
    LivePeer.uploadContent(video_path, assetUrl['url'])

    return assetUrl


def main() -> None:
    if len(sys.argv) != 2:
        print(sys.argv)
        print("Usage: python3 upload-video.py /path/to/directory_or_video")
        sys.exit(1)

    LivePeer = LivePeerSDK(os.getenv("LIVEPEER_API_KEY"))
    assetUrl = upload_video(LivePeer, sys.argv[1])

    video_name = os.path.basename(sys.argv[1])
    process_file(video_name, assetUrl, LivePeer)


if __name__ == '__main__':
    main()
