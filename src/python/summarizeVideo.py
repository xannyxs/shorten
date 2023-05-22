import argparse
import os
import sys
import subprocess
from typing import Any

import whisper
import openai


def process_text_file(transcribed_text: str) -> str:
    content = transcribed_text.replace('um', '').replace('uh', '').replace(',', '').replace('  ', ' ')

    words = content.split()
    word_count = len(words)

    if word_count > 1700:
        print('Content too long, will trim file')
        words = words[:1700]
        content = ' '.join(words)

    return content


def summarize_text(input_text: str, output_file: str) -> None:
    openai.api_key = os.environ.get('CHATGPT_API_KEY')

    response = openai.ChatCompletion.create( # type: ignore
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Summarize this for a description for a video:\n\n{input_text}"}
        ],
        temperature=0.4,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    summary = response.choices[0].message["content"].strip()
    if os.path.exists(output_file):
        with open(output_file, 'w') as file:
            file.write(summary)
    else:
        with open(output_file, 'x') as file:
            file.write(summary)


def download_m3u8_video_as_wav(m3u8_url: str, output_name: str) -> None:
    command = [
        "ffmpeg",
        "-analyzeduration", "100M",
        "-probesize", "100M",
        "-i", m3u8_url,
        "-vn",
        "-c:a", "pcm_s16le",
        "-ar", "44100",
        f'{output_name}.wav'
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Successfully downloaded and converted audio from {m3u8_url} to {output_name}.wav")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while downloading and converting audio from {m3u8_url} to {output_name}.wav: {e}")


def convert_speech_to_text(input_wav: str) -> Any:
    model = whisper.load_model("base")
    result = model.transcribe(input_wav)
    text = result["text"]

    print(f"Successfully saved speech-to-text result")
    return text


def start_summary(playbackUrl: str, temp_file_path: str) -> None:
    download_m3u8_video_as_wav(playbackUrl, temp_file_path)
    transcribed_text = convert_speech_to_text(f"{temp_file_path}.wav")
    shortend_text = process_text_file(transcribed_text)
    summarize_text(shortend_text, f'{temp_file_path}.txt')
