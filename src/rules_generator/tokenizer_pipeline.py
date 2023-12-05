from typing import List

from botok.tokenizers.wordtokenizer import WordTokenizer

from rules_generator.data_processor import (
    remove_all_spaces,
    remove_spaces_for_tokenization,
)
from rules_generator.Token import Token


def botok_word_tokenizer_pipeline(gold_corpus: str, split_affixes=True) -> List[Token]:
    words_joined_corpus = remove_spaces_for_tokenization(gold_corpus)

    """
    input: text string
    output/return: list of tokens
    """
    tokenizer = WordTokenizer()
    botok_tokens = tokenizer.tokenize(words_joined_corpus, split_affixes=split_affixes)
    tokens = [
        Token(text=remove_all_spaces(token.text), pos=token.pos)
        for token in botok_tokens
    ]

    return tokens


if __name__ == "__main__":
    tokens = botok_word_tokenizer_pipeline(
        "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ-འི་ ཕྲེང་བ།  ༄༅༅། །རྒྱ་གར་ སྐད་དུ།"
    )
    for token in tokens:
        print(token.text, token.pos)
