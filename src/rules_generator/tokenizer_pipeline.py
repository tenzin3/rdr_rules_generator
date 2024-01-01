from typing import Iterator

from botok.tokenizers.wordtokenizer import WordTokenizer

from rules_generator.data_processor import (
    remove_all_spaces,
    remove_spaces_for_tokenization,
)
from rules_generator.Token import Token
from rules_generator.utility import measure_execution_time


@measure_execution_time(custom_name="Tokenization")
def botok_word_tokenizer_pipeline(
    gold_corpus: str, split_affixes=True
) -> Iterator[Token]:
    words_joined_corpus = remove_spaces_for_tokenization(gold_corpus)

    """
    input: text string
    output/return: list of tokens
    """
    tokenizer = WordTokenizer()
    botok_tokens = tokenizer.tokenize(words_joined_corpus, split_affixes=split_affixes)

    for token in botok_tokens:
        yield Token(text=remove_all_spaces(token.text), pos=token.pos)
