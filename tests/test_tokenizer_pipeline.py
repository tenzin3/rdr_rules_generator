from rules_generator.tokenizer_pipeline import botok_word_tokenizer_pipeline


def test_botok_word_tokenizer_pipeline():
    string = "ང་བོད་པ་ཡིན།"
    tokens = botok_word_tokenizer_pipeline(string)
    curr_token = next(tokens)
    assert curr_token.text == "ང་"
    assert curr_token.pos == "PRON"

    curr_token = next(tokens)
    assert curr_token.text == "བོད་པ་"
    assert curr_token.pos == "PROPN"

    curr_token = next(tokens)
    assert curr_token.text == "ཡིན"
    assert curr_token.pos == "NO_POS"

    curr_token = next(tokens)
    assert curr_token.text == "།"
    assert curr_token.pos == ""
