from typing import List

from botok import TSEK

from rules_generator.config import (
    AFFIXES,
    AFFIXES_WITH_TSEK,
    AFFIXES_WITHOUT_TSEK,
    PUNCTS,
)
from rules_generator.tokenizer_pipeline import Token
from rules_generator.utility import get_syllables


def find_next_matching_token(
    tokenized_tokens: List[Token], index: int, corpus_tokens: List[Token], idx: int
):
    def get_combined_text(tokens, end):
        """Get the combined text of the tokens up to the given end index."""
        return "".join([token.text for token in tokens[: end + 1]])

    tokenized_len = len(tokenized_tokens)
    corpus_len = len(corpus_tokens)
    while index < tokenized_len and idx < corpus_len:
        matching_cond = tokenized_tokens[index].text == corpus_tokens[idx].text
        tokenized_text_len = len(get_combined_text(tokenized_tokens, index))
        corpus_text_len = len(get_combined_text(corpus_tokens, idx))

        length_cond = tokenized_text_len == corpus_text_len
        if matching_cond and length_cond:
            break
        if tokenized_text_len == corpus_text_len:
            index += 1
            idx += 1
        elif tokenized_text_len <= corpus_text_len:
            index += 1
        else:
            idx += 1

    if index == tokenized_len or idx == corpus_len:
        return tokenized_len, corpus_len

    return index, idx


def tagger(tokenized_tokens: List[Token], corpus_tokens: List[Token]) -> List[Token]:
    index = 0
    idx = 0
    while index < len(tokenized_tokens) and idx < len(corpus_tokens):
        token = tokenized_tokens[index]
        if token.text == corpus_tokens[idx].text:
            tokenized_tokens[index].tag = "U"
            idx += 1
            index += 1
            continue
        # find the next correctly segmented token
        next_index, next_idx = find_next_matching_token(
            tokenized_tokens, index, corpus_tokens, idx
        )
        # tag the unmatched tokens in gold corpus
        unmatched_tokens = []
        for i in range(idx, next_idx):
            syls = get_syllables(corpus_tokens[i].text)
            for num, syl in enumerate(syls):
                tag = "B" if num == 0 else "I"
                unmatched_tokens.append((syl, tag))
                if syl not in AFFIXES and syl.endswith(tuple(AFFIXES)):
                    unmatched_tokens.append((syl, tag))
        # Join for affixes
        condition = False
        for u_idx, (syl, tag) in enumerate(unmatched_tokens):
            if u_idx == 0:
                continue
            prev_syl, prev_tag = unmatched_tokens[u_idx - 1]
            if prev_syl.endswith(TSEK):
                continue

            if syl.endswith(tuple(AFFIXES_WITH_TSEK)):
                condition = True
            elif syl.endswith(tuple(AFFIXES_WITHOUT_TSEK)):
                if u_idx < len(unmatched_tokens) - 1:
                    next_syl = unmatched_tokens[u_idx + 1][0]
                    if any(punct in next_syl for punct in PUNCTS):
                        condition = True
            if condition:
                if prev_tag == "B":
                    unmatched_tokens[u_idx - 1] = (prev_syl + syl, "X")
                else:
                    unmatched_tokens[u_idx - 1] = (prev_syl + syl, "Y")

                del unmatched_tokens[u_idx]
                condition = False

        # tag the unmatched tokens in tokenized corpus
        unmatched_token_count = 0
        for j in range(index, next_index):
            syls = get_syllables(tokenized_tokens[j].text)

            curr_tag = ""
            for num, syl in enumerate(syls):
                curr_tag += unmatched_tokens[unmatched_token_count][1]
                unmatched_token_count += 1

            tokenized_tokens[j].tag = curr_tag
        # update the index and idx
        index = next_index
        idx = next_idx

    return tokenized_tokens
