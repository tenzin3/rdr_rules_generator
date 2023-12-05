from rules_generator.data_processor import (
    keep_only_tibetan_characters,
    remove_spaces_for_tokenization,
    separate_punctuations_for_tagging,
)


def test_keep_only_tibetan_characters():
    english_text = "helloworld"
    expected_result = ""
    result = keep_only_tibetan_characters(english_text)
    assert result == expected_result

    tibetan_text = "ཞི་བདེ"
    expected_result = "ཞི་བདེ"
    result = keep_only_tibetan_characters(tibetan_text)
    assert result == expected_result

    mixed_text = "peace ཞི་བདེ."
    expected_result = " ཞི་བདེ"
    result = keep_only_tibetan_characters(mixed_text)
    assert result == expected_result

    mixed_text_with_newline = "peace\nཞི་བདེ."
    expected_result = "\nཞི་བདེ"
    result = keep_only_tibetan_characters(mixed_text_with_newline)
    assert result == expected_result


def test_remove_spaces_for_tokenization():
    only_words = "ཞི་བདེ ཞི་བདེ   ཞི་བདེ"
    expected_result = "ཞི་བདེཞི་བདེཞི་བདེ"
    result = remove_spaces_for_tokenization(only_words)
    assert result == expected_result

    words_and_puncts = "༄༅༅། །རྒྱ་གར་ སྐད་དུ།"
    expected_result = "༄༅༅། ། རྒྱ་གར་སྐད་དུ །"
    result = remove_spaces_for_tokenization(words_and_puncts)
    assert result == expected_result


def test_separate_punctuations_for_tagging():
    words_and_puncts = "༄༅༅། །རྒྱ་གར་ སྐད་དུ།"
    expected_result = "༄༅༅།། རྒྱ་གར་ སྐད་དུ །"
    result = separate_punctuations_for_tagging(words_and_puncts)
    assert result == expected_result
