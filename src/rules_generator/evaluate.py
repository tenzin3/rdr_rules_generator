import json

from rules_generator.config import CLOSING_PUNCTS
from rules_generator.data_processor import separate_punctuations_for_tagging


def get_word_segmented_text(json_file_path) -> str:
    with open(json_file_path) as json_file:
        json_content = json.load(json_file)

    modified_text_file = json_content.get("modified_text", [])
    # Use list comprehensions to flatten the nested list and join the words with spaces.
    word_segmented_text = ""
    for modified_text_line in modified_text_file:
        if modified_text_line:
            word_segmented_text += " ".join(modified_text_line)

    return word_segmented_text


def write_word_segmented_json_to_txt(json_file_path, txt_file_path):
    word_segmented_text = get_word_segmented_text(json_file_path)
    word_segmented_text = separate_punctuations_for_tagging(word_segmented_text)

    word_splited = word_segmented_text.strip().split()
    curr_line_text = ""

    with open(txt_file_path, "w") as txt_file:
        for word in word_splited:
            curr_line_text += f"{word} "
            if any(punct in word for punct in CLOSING_PUNCTS) and curr_line_text:
                txt_file.write(curr_line_text.strip() + "\n")
                curr_line_text = ""

        if curr_line_text:
            txt_file.write(curr_line_text.strip() + "\n")
