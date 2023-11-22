import re
from typing import Union

from botok.tokenizers.wordtokenizer import WordTokenizer
from pydantic import BaseModel, Field, field_validator

from rules_generator.data_processor import (
    remove_all_spaces,
    remove_spaces_for_tokenization,
)


class Token(BaseModel):
    text: str
    pos: Union[str, None] = Field(default=None)
    tag: Union[str, None] = Field(default=None, validate_default=False)

    @field_validator("text")
    @classmethod
    def text_must_be_tibetan(cls, v):
        tibetan_regex = r"^[\u0F00-\u0FFF]+$"
        if not re.match(tibetan_regex, v):
            raise ValueError("Text must contain only Tibetan characters")
        return v

    @field_validator("tag")
    @classmethod
    def tag_must_be_BIUXY(cls, v):
        if not all(char in "BIUXY" for char in v):
            raise ValueError("Tag must contain only BIUXY")
        return v

    def __str__(self):
        return f"Token(text={self.text}, pos={self.pos})"


def botok_word_tokenizer_pipeline(gold_corpus: str, split_affixes=True):
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
