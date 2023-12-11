from pathlib import Path
from typing import Iterator, List

from rules_generator.config import DATA_DIR, PUNCTS
from rules_generator.data_processor import (
    remove_all_spaces,
    separate_punctuations_for_tagging,
)
from rules_generator.tagger import tagger
from rules_generator.Token import LineTagger, Token
from rules_generator.tokenizer_pipeline import botok_word_tokenizer_pipeline
from rules_generator.utility import (
    measure_execution_time,
    write_tokens_to_json_file,
    write_tokens_to_text_file,
)


def join_tokens_in_sentence(tokens: Iterator[Token]) -> Iterator[LineTagger]:
    """
    Joining the tokens if the tokens are in the same sentence.
    Achieved by looping through all tokens and checking if the token contains
     any punctuation.

     Actual puntuation is not included in the tokens in this phase.
    """
    new_tokens_line: List[Token] = []
    for token in tokens:
        punct_found = False
        for punct in PUNCTS:
            if punct in token.text:
                punct_found = True
                if new_tokens_line:
                    yield LineTagger(
                        text="".join([t.text for t in new_tokens_line]),
                        tokens=new_tokens_line,
                    )
                    new_tokens_line = []
                    break
                else:
                    break
        if not punct_found:
            new_tokens_line.append(token)
    if new_tokens_line:
        yield LineTagger(
            text="".join([t.text for t in new_tokens_line]),
            tokens=new_tokens_line,
        )


@measure_execution_time(custom_name="Tagging")
def line_by_line_tagger(
    gold_corpus: str, split_affixes: bool = True
) -> Iterator[LineTagger]:
    # tokenize with botok as List[Token] dtype
    tokenized_tokens = botok_word_tokenizer_pipeline(gold_corpus, split_affixes)

    # get gold corpus tokens as List[Token] dtype
    gold_corpus = separate_punctuations_for_tagging(gold_corpus)
    gold_corpus_tokens = (
        Token(text=remove_all_spaces(token_text)) for token_text in gold_corpus.split()
    )

    """
    Joining the tokens if the tokens are in the same sentence.
    Achieved by looping through all tokens and checking if the token contains
     any punctuation.
    """

    tokenized_lines = join_tokens_in_sentence(tokenized_tokens)
    gold_corpus_lines = join_tokens_in_sentence(gold_corpus_tokens)

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

    for line_of_tokenized_tokens, line_of_gold_corpus_tokens in zip(
        tokenized_lines, gold_corpus_lines
    ):
        try:
            # Attempt to tag the line
            line_of_tokenized_tokens.tokens = tagger(
                line_of_tokenized_tokens.tokens, line_of_gold_corpus_tokens.tokens
            )
            yield line_of_tokenized_tokens
        except:  # noqa
            # Print the text of the line where an error occurred
            print("Error occured in line:", line_of_tokenized_tokens.text)
    # Return only successfully tagged lines


if __name__ == "__main__":
    gold_corpus = Path(DATA_DIR / "TIB_train.txt").read_text(encoding="utf-8")
    tagged_tokens = line_by_line_tagger(gold_corpus)
    write_tokens_to_text_file(tagged_tokens, Path(DATA_DIR / "tagged_tokens.txt"))
    write_tokens_to_json_file(tagged_tokens, Path(DATA_DIR / "tagged_tokens.json"))
