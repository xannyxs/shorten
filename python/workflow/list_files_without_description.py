import json
from typing import List

import glob


def list_files_without_description(batch_size: int = 10) -> List[List[str]]:
    files_without_description: List[str] = []

    for file_path in glob.glob('./streameth-platform/data/session/**/*.JSON', recursive=True):
        with open(file_path, 'r') as f:
            data = json.load(f)
            if not data.get('gpt_description') or data['gpt_description'].strip() == '':
                files_without_description.append(file_path)

    batches: List[List[str]] = [files_without_description[i:i+batch_size]
                                for i in range(0, len(files_without_description), batch_size)]

    return batches


if __name__ == "__main__":
    batches = list_files_without_description()

    print(json.dumps(batches))
