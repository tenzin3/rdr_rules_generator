from pathlib import Path
from typing import List

from rules_generator.config import DATA_DIR, PUNCTS
from rules_generator.data_processor import (
    remove_all_spaces,
    separate_punctuations_for_tagging,
)
from rules_generator.tagger import tagger
from rules_generator.Token import LineTagger, Token
from rules_generator.tokenizer_pipeline import botok_word_tokenizer_pipeline
from rules_generator.utility import write_tokens_to_json_file, write_tokens_to_text_file


def join_tokens_in_sentence(tokens: List[Token]) -> List[LineTagger]:
    """
    Joining the tokens if the tokens are in the same sentence.
    Achieved by looping through all tokens and checking if the token contains
     any punctuation.

     Actual puntuation is not included in the tokens in this phase.
    """
    line_tagger_list = []
    new_tokens_line: List[Token] = []
    for token in tokens:
        punct_found = False
        for punct in PUNCTS:
            if punct in token.text:
                punct_found = True
                if new_tokens_line:
                    line_tagger_list.append(
                        LineTagger(
                            text="".join([token.text for token in new_tokens_line]),
                            tokens=new_tokens_line,
                        )
                    )
                    new_tokens_line = []
                    break
                else:
                    break
        if not punct_found:
            new_tokens_line.append(token)
    return line_tagger_list


def line_by_line_tagger(gold_corpus: str) -> List[LineTagger]:
    # tokenize with botok as List[Token] dtype
    print("1.TOKENIZING PROCESS STARTED::::>>>>")
    tokenized_tokens = botok_word_tokenizer_pipeline(gold_corpus)

    # get gold corpus tokens as List[Token] dtype
    gold_corpus = separate_punctuations_for_tagging(gold_corpus)
    gold_corpus_tokens = [
        Token(text=remove_all_spaces(token_text)) for token_text in gold_corpus.split()
    ]

    """
    Joining the tokens if the tokens are in the same sentence.
    Achieved by looping through all tokens and checking if the token contains
     any punctuation.
    """

    tokenized_tokens = join_tokens_in_sentence(tokenized_tokens)
    gold_corpus_tokens = join_tokens_in_sentence(gold_corpus_tokens)
    print("1.TOKENIZING PROCESS ENDED::::>>>>")
    if len(tokenized_tokens) != len(gold_corpus_tokens):
        raise ValueError("Number of lines are not equal")

    """
    Tagging the tokens in tokenized_tokens comparing with gold_corpus_tokens using
    tagger function.
    Here we are doing line by line tagging and if any problems occurs
    in tagging the line, the error field in the LineTagger class will be set to True.
    Error might occur due to
    i) mismatch or loss of text
    ii) uncommon positioning of tsek
    iii) incorrect way of spliting  of affixes
    """
    print("2.TAGGING PROCESS STARTED::::>>>>")
    # Initialize a list to hold successfully tagged lines
    successfully_tagged_tokens = []
    for line_of_tokenized_tokens, line_of_gold_corpus_tokens in zip(
        tokenized_tokens, gold_corpus_tokens
    ):
        try:
            # Attempt to tag the line
            line_of_tokenized_tokens.tokens = tagger(
                line_of_tokenized_tokens.tokens, line_of_gold_corpus_tokens.tokens
            )
            successfully_tagged_tokens.append(line_of_tokenized_tokens)
        except:  # noqa
            # Print the text of the line where an error occurred
            print("Error occured in line:", line_of_tokenized_tokens.text)
    print("2.TAGGING PROCESS ENDED::::>>>>")
    # Return only successfully tagged lines
    return successfully_tagged_tokens


if __name__ == "__main__":
    gold_corpus = Path(DATA_DIR / "TIB_train.txt").read_text(encoding="utf-8")
    tagged_tokens = line_by_line_tagger(gold_corpus)
    write_tokens_to_text_file(tagged_tokens, Path(DATA_DIR / "tagged_tokens.txt"))
    write_tokens_to_json_file(tagged_tokens, Path(DATA_DIR / "tagged_tokens.json"))
