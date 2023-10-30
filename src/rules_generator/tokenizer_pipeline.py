from botok.tokenizers.wordtokenizer import WordTokenizer

from rules_generator.data_processor import remove_spaces_for_tokenization


class Token:
    def __init__(self, text, pos=None):
        self.text = text
        self.pos = pos

    def __str__(self):
        return f"Token(text={self.text}, pos={self.pos})"


def botok_word_tokenizer_pipeline(gold_corpus: str, split_affixes=False):
    words_joined_corpus = remove_spaces_for_tokenization(gold_corpus)

    """
    input: text string
    output/return: list of tokens
    """
    tokenizer = WordTokenizer()
    botok_tokens = tokenizer.tokenize(words_joined_corpus, split_affixes=split_affixes)
    tokens = [Token(token.text.strip(), token.pos) for token in botok_tokens]

    return tokens


if __name__ == "__main__":
    tokens = botok_word_tokenizer_pipeline(
        "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ-འི་ ཕྲེང་བ།  ༄༅༅། །རྒྱ་གར་ སྐད་དུ།"
    )
    print(tokens)
