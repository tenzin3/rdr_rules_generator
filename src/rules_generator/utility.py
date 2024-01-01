import json
import time
from functools import wraps
from pathlib import Path
from typing import List, Union

from botok import TSEK

from rules_generator.Token import LineTagger


def count_syllables(text: str) -> int:
    return len([element for element in text.split(TSEK) if element.strip() != ""])


def get_syllables(text: str) -> List[str]:
    text
    tsek_split_text = text.split(TSEK)
    text_syllables = [syl + TSEK for syl in tsek_split_text[:-1] if syl != ""]
    if tsek_split_text[-1] != "":
        text_syllables.append(tsek_split_text[-1])
    return text_syllables


def write_tokens_to_text_file(tokens: List[LineTagger], file_path: Union[str, Path]):
    file_path = Path(file_path)
    if file_path.suffix != ".txt":
        raise ValueError("The file path must be a .txt file.")

    with open(file_path, "w", encoding="utf-8") as f:
        for line_token in tokens:
            for token in line_token.tokens:
                f.write(rf"{token.text}/{token.tag} ")
            f.write("\n")


def write_tokens_to_json_file(tokens: List[LineTagger], file_path: Union[str, Path]):
    file_path = Path(file_path)
    if file_path.suffix != ".json":
        raise ValueError("The file path must be a .json file.")

    with open(file_path, "w", encoding="utf-8") as f:
        # Serialize the list of LineTagger objects to JSON and write to file
        json_data = json.dumps(
            [token.model_dump() for token in tokens], ensure_ascii=False, indent=4
        )
        f.write(json_data)


def read_tokens_from_json_file(file_path: Union[str, Path]) -> List[LineTagger]:
    file_path = Path(file_path)
    if file_path.suffix != ".json":
        raise ValueError("The file path must be a .json file.")

    with open(file_path, encoding="utf-8") as f:
        # Deserialize the JSON data back into LineTagger objects
        data = json.load(f)
        return [LineTagger(**item) for item in data]


def measure_execution_time(custom_name=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            name = custom_name if custom_name else func.__name__
            print(f"Total time taken for {name}: {end_time - start_time} seconds.")
            return result

        return wrapper

    return decorator
