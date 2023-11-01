from rules_generator.tagger import tagger


def test_tagger():
    correctly_segmented_words = "ང་ བོད་པ་ ཡིན །"
    tagged_tokens = tagger(correctly_segmented_words)
    assert tagged_tokens[0].text == "ང་"
    assert tagged_tokens[0].tag == "U"
    assert tagged_tokens[1].text == "བོད་པ་"
    assert tagged_tokens[1].tag == "U"
    assert tagged_tokens[2].text == "ཡིན"
    assert tagged_tokens[2].tag == "U"
    assert tagged_tokens[3].text == "།"
    assert tagged_tokens[3].tag == "U"

    incorrectly_segmented_words = "ལ་ ལ་ལ་ ལ་ལ་"
    tagged_tokens = tagger(incorrectly_segmented_words)
    assert tagged_tokens[0].text == "ལ་ལ་"
    assert tagged_tokens[0].tag == "BB"
    assert tagged_tokens[1].text == "ལ་ལ་"
    assert tagged_tokens[1].tag == "IB"

    incorrectly_joined_affix = "རིན་པོ་ཆེའི་"
    tagged_tokens = tagger(incorrectly_joined_affix)
    assert tagged_tokens[0].text == "རིན་པོ་ཆེ"
    assert tagged_tokens[0].tag == "BII"
    assert tagged_tokens[1].text == "འི་"
    assert tagged_tokens[1].tag == "I"

    incorrectly_split_affix = "ཡོང ས་ སུ་"
    tagged_tokens = tagger(incorrectly_split_affix)
    assert tagged_tokens[0].text == "ཡོངས་སུ་"
    assert tagged_tokens[0].tag == "XB"


if __name__ == "__main__":
    gold_corpus = "ང་ བོད་པ་ ཡིན །"
    tagged_tokens = tagger(gold_corpus)
    for token in tagged_tokens:
        print(f"{token.text} {token.tag}")
