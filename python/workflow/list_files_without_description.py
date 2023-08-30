import json
import glob
from typing import List, Dict, Any

def list_files_without_description(batch_size: int = 10) -> List[Dict[str, Any]]:
    files_without_description: List[str] = []

    # Explicitly annotate the type of file_paths
    file_paths: List[str] = glob.glob('./streameth-platform/data/sessions/ethberlin_2022/*.json', recursive=True)

    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data: Dict[str, Any] = json.load(f)
            if not data.get('gpt_description') or data['gpt_description'].strip() == '' or not data.get('description') or data['description'].strip() == '':
                files_without_description.append(file_path)

    # Explicitly annotate the type of batches
    batches: List[Dict[str, Any]] = []
    for i in range(0, len(files_without_description), batch_size):
        batch: Dict[str, Any] = {
            "batchID": i // batch_size + 1,  # batchID starting from 1
            "files": files_without_description[i:i + batch_size]
        }
        batches.append(batch)

    return batches

if __name__ == "__main__":
    batches: List[Dict[str, Any]] = list_files_without_description()
    print(json.dumps(batches))
