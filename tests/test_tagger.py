from rules_generator.data_processor import (
    remove_all_spaces,
    separate_punctuations_for_tagging,
)
from rules_generator.tagger import tagger
from rules_generator.Token import Token
from rules_generator.tokenizer_pipeline import botok_word_tokenizer_pipeline


def get_tokenized_and_gold_corpus_tokens(text: str):
    tokenized_tokens = botok_word_tokenizer_pipeline(text)
    gold_corpus = separate_punctuations_for_tagging(text)
    gold_corpus_tokens = [
        Token(text=remove_all_spaces(token_text)) for token_text in gold_corpus.split()
    ]
    return list(tokenized_tokens), list(gold_corpus_tokens)


def test_tagger():
    correctly_segmented_words = "ང་ བོད་པ་ ཡིན །"
    tokenized_tokens, gold_corpus_tokens = get_tokenized_and_gold_corpus_tokens(
        correctly_segmented_words
    )
    tagged_tokens = tagger(tokenized_tokens, gold_corpus_tokens)

    assert tagged_tokens[0].text == "ང་"
    assert tagged_tokens[0].tag == "U"
    assert tagged_tokens[1].text == "བོད་པ་"
    assert tagged_tokens[1].tag == "U"
    assert tagged_tokens[2].text == "ཡིན"
    assert tagged_tokens[2].tag == "U"
    assert tagged_tokens[3].text == "།"
    assert tagged_tokens[3].tag == "U"

    incorrectly_segmented_words = "ལ་ ལ་ལ་ ལ་ལ་"
    tokenized_tokens, gold_corpus_tokens = get_tokenized_and_gold_corpus_tokens(
        incorrectly_segmented_words
    )
    tagged_tokens = tagger(tokenized_tokens, gold_corpus_tokens)
    assert tagged_tokens[0].text == "ལ་ལ་"
    assert tagged_tokens[0].tag == "BB"
    assert tagged_tokens[1].text == "ལ་ལ་"
    assert tagged_tokens[1].tag == "IB"

    incorrectly_joined_affix = "རིན་པོ་ཆེའི་"
    tokenized_tokens, gold_corpus_tokens = get_tokenized_and_gold_corpus_tokens(
        incorrectly_joined_affix
    )
    tagged_tokens = tagger(tokenized_tokens, gold_corpus_tokens)

    assert tagged_tokens[0].text == "རིན་པོ་ཆེ"
    assert tagged_tokens[0].tag == "BII"
    assert tagged_tokens[1].text == "འི་"
    assert tagged_tokens[1].tag == "I"

    incorrectly_split_affix = "ཡོང ས་ སུ་"
    tokenized_tokens, gold_corpus_tokens = get_tokenized_and_gold_corpus_tokens(
        incorrectly_split_affix
    )
    tagged_tokens = tagger(tokenized_tokens, gold_corpus_tokens)

    assert tagged_tokens[0].text == "ཡོངས་སུ་"
    assert tagged_tokens[0].tag == "XB"
