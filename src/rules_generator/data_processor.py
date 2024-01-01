import re

from botok import TSEK

from rules_generator.config import PUNCTS_CHAR_SET


def normalise_space(text: str) -> str:
    pattern = r"\s+"
    replacement = " "
    text = re.sub(pattern, replacement, text)
    return text


def remove_all_spaces(text: str) -> str:
    pattern = r"\s+"
    replacement = ""
    text = re.sub(pattern, replacement, text)
    return text


def normalise_tsek(text: str) -> str:
    # there are no tsek, we are using botok's tsek
    return re.sub(r"[་༌]", TSEK, text)


def keep_only_tibetan_characters(text: str) -> str:
    return re.sub(r"[^\u0F00-\u0FFF\s\n\t]+", r"", text)


def clean_text(text: str) -> str:
    text = keep_only_tibetan_characters(text)
    text = normalise_space(text)
    text = normalise_tsek(text)
    return text


def add_spaces_around_punctuation(text: str) -> str:
    patterns = [
        # put space between punctuation and others
        (rf"([^{PUNCTS_CHAR_SET}\s])([{PUNCTS_CHAR_SET}])", r"\1 \2"),
        (rf"([{PUNCTS_CHAR_SET}])([^{PUNCTS_CHAR_SET}\s])", r"\1 \2"),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)

    return text


def remove_spaces_for_tokenization(gold_corpus: str) -> str:
    gold_corpus = clean_text(gold_corpus)
    gold_corpus = add_spaces_around_punctuation(gold_corpus)

    """
    input: gold corpus where words are separated by space
    output/return: corpus string where words are joined together
    """

    patterns = [
        # join tibetan words unless for punct
        (rf"([^{PUNCTS_CHAR_SET}])\s+([^{PUNCTS_CHAR_SET}])", r"\1\2")
    ]

    for pattern, replacement in patterns:
        gold_corpus = re.sub(pattern, replacement, gold_corpus)

    return gold_corpus


def separate_punctuations_for_tagging(gold_corpus: str) -> str:
    gold_corpus = clean_text(gold_corpus)
    gold_corpus = add_spaces_around_punctuation(gold_corpus)

    """
    input: gold corpus where words are separated by space
    output/return: separting punctuations from words and joining punctuations together
    """
    patterns = [
        (rf"([{PUNCTS_CHAR_SET}])\s+([{PUNCTS_CHAR_SET}])", r"\1\2"),
    ]

    for pattern, replacement in patterns:
        gold_corpus = re.sub(pattern, replacement, gold_corpus)

    return gold_corpus
