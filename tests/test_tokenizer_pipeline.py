from rules_generator.tokenizer_pipeline import botok_word_tokenizer_pipeline


def test_botok_word_tokenizer_pipeline():
    string = "ང་བོད་པ་ཡིན།"
    tokens = botok_word_tokenizer_pipeline(string)
    assert tokens[0].text == "ང་"
    assert tokens[1].text == "བོད་པ་"
    assert tokens[2].text == "ཡིན"
    assert tokens[3].text == "།"

    assert tokens[0].pos == "PRON"
    assert tokens[1].pos == "PROPN"
    assert tokens[2].pos == "NO_POS"
    assert tokens[3].pos == ""
