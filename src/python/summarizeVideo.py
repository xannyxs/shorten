import os
import subprocess
from typing import Any

import whisper
import openai

from utils import eprint
from sentence_transformers import SentenceTransformer, util

GPT_MODEL = "gpt-3.5-turbo-16k"
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
OPENAI_API_KEY = os.getenv('CHATGPT_API_KEY')
if not OPENAI_API_KEY:
    raise EnvironmentError("CHATGPT_API_KEY environment variable not set")


def process_text_file(transcribed_text: str) -> str:
    replacements = ['um', 'uh', ',', '  ']
    content = transcribed_text
    for r in replacements:
        content = content.replace(r, '')

    return content


def generate_summary(input_text: str, temperature: float) -> Any:
    response = openai.ChatCompletion.create(  # type: ignore
        model=GPT_MODEL,
        messages=[{
            "role":
            "user",
            "content":
            f"Summarize this text delimited by triple single quotes for a description for a "
            f"video:\n\n'''{input_text}'''"
        }],
        temperature=temperature,
        max_tokens=512,
        frequency_penalty=0.3,
        presence_penalty=0)
    return response['choices'][0]['message']['content']


def summarize_text(input_text: str, output_file: str) -> None:
    openai.api_key = OPENAI_API_KEY

    # Generate summaries with different temperatures
    summaries = [
        generate_summary(input_text, temp) for temp in [0.3, 0.5, 0.7]
    ]

    summary_input_text = "\n\n\n'''".join(summaries)
    summary_of_summaries = generate_summary(summary_input_text, 0.4)

    # is_valid = check_summary_validity(input_text, summary_of_summaries)
    # if not is_valid:
    #     eprint("Summary is invalid")
    #     sys.exit(1)

    with open(output_file, 'w') as file:
        file.write(summary_of_summaries)


def check_summary_validity(input_text: str, summary: str) -> bool:
    model = SentenceTransformer(EMBEDDING_MODEL)

    input_embedding = model.encode(input_text, convert_to_tensor=True)
    summary_embedding = model.encode(summary, convert_to_tensor=True)

    similarity = util.pytorch_cos_sim(input_embedding, summary_embedding)

    return similarity.item() > 0.5  # type: ignore


def download_m3u8_video_as_wav(m3u8_url: str, output_name: str) -> None:
    command = [
        "ffmpeg", "-analyzeduration", "100M", "-probesize", "100M", "-i",
        m3u8_url, "-vn", "-c:a", "pcm_s16le", "-ar", "44100",
        f'{output_name}.wav'
    ]

    try:
        subprocess.run(command, check=True)
        print(
            f"Successfully downloaded and converted audio from {m3u8_url} to {output_name}.wav"
        )
    except subprocess.CalledProcessError as e:
        eprint(
            f"Error occurred while downloading and converting audio from {m3u8_url} to {output_name}.wav: {e}"
        )


def convert_speech_to_text(input_wav: str) -> Any:
    model = whisper.load_model("base")
    result = model.transcribe(input_wav)
    text = result["text"]

    print("Successfully saved speech-to-text result")
    return text


def start_summary(playbackUrl: str, temp_file_path: str) -> None:
    download_m3u8_video_as_wav(playbackUrl, temp_file_path)
    transcribed_text = convert_speech_to_text(f"{temp_file_path}.wav")
    shortend_text = process_text_file(transcribed_text)
    summarize_text(shortend_text, f'{temp_file_path}.txt')
