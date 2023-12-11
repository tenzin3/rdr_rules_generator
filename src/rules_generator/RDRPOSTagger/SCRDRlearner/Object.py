from typing import Dict, Iterator, List, Optional

from rules_generator.Token import LineTagger, Token


class Object:
    attributes = [
        "word",
        "tag",
        "pos",
        "prevWord2",
        "prevWord1",
        "nextWord1",
        "nextWord2",
        "prevPos2",
        "prevPos1",
        "nextPos1",
        "nextPos2",
    ]

    def __init__(self, *args):
        for attr, value in zip(self.attributes, args):
            setattr(self, attr, value)

    def toStr(self):
        res = "("
        for att in self.attributes:
            boo = isinstance(getattr(self, att), str)
            if not boo:
                res = res + str(getattr(self, att))
            else:
                res = res + '"' + str(getattr(self, att)) + '"'

            if att != self.attributes[-1]:
                res = res + ","
        res += ")"
        return res


def getWordTag(wordTag):
    if wordTag == "///":
        return "/", "/"
    index = wordTag.rfind("/")
    if index == -1:
        return None, None
    word = wordTag[:index].strip()
    tag = wordTag[index + 1 :].strip()  # noqa
    return word, tag


def getObject(tokens: List[Token], index):  # Sequence of "Word/Tag"
    preWord1 = prePos1 = preWord2 = prePos2 = ""
    nextWord1 = nextPos1 = nextWord2 = nextPos2 = ""

    word, tag, pos = tokens[index].text, tokens[index].tag, tokens[index].pos
    if index > 0:
        preWord1, prePos1 = tokens[index - 1].text, tokens[index - 1].pos
    if index > 1:
        preWord2, prePos2 = tokens[index - 2].text, tokens[index - 2].pos
    if index < len(tokens) - 1:
        nextWord1, nextPos1 = tokens[index + 1].text, tokens[index + 1].pos
    if index < len(tokens) - 2:
        nextWord2, nextPos2 = tokens[index + 2].text, tokens[index + 2].pos

    return Object(
        word,
        tag,
        pos,
        preWord2,
        preWord1,
        nextWord1,
        nextWord2,
        prePos2,
        prePos1,
        nextPos1,
        nextPos2,
    )


def getObjectDictionary(tagged_tokens: Iterator[LineTagger]):
    objects: Dict[str, Dict[str, List]] = {}

    for line_of_tokens in tagged_tokens:

        for index, token in enumerate(line_of_tokens.tokens):
            correctTag = token.tag if token.tag is not None else ""
            initTag = "U"
            if initTag not in objects.keys():
                objects[initTag] = {}
                objects[initTag][initTag] = []

            if correctTag not in objects[initTag].keys():
                objects[initTag][correctTag] = []

            objects[initTag][correctTag].append(getObject(line_of_tokens.tokens, index))

    return objects


class FWObject:
    """
    RDRPOSTaggerV1.1: new implementation scheme
    RDRPOSTaggerV1.2: add suffixes
    """

    def __init__(self, check=False):
        self.context: List[Optional[str]] = [None] * 10  # Explicitly type hinting
        if check:
            i = 0
            while i < 10:
                self.context[i] = "<W>"
                self.context[i + 1] = "<T>"
                i = i + 2

        self.notNoneIds = []

    @staticmethod
    def getFWObject(startWordTags, index):
        object = FWObject(True)
        word, tag = getWordTag(startWordTags[index])
        object.context[4] = word
        object.context[5] = tag

        if index > 0:
            preWord1, preTag1 = getWordTag(startWordTags[index - 1])
            object.context[2] = preWord1
            object.context[3] = preTag1

        if index > 1:
            preWord2, preTag2 = getWordTag(startWordTags[index - 2])
            object.context[0] = preWord2
            object.context[1] = preTag2

        if index < len(startWordTags) - 1:
            nextWord1, nextTag1 = getWordTag(startWordTags[index + 1])
            object.context[6] = nextWord1
            object.context[7] = nextTag1

        if index < len(startWordTags) - 2:
            nextWord2, nextTag2 = getWordTag(startWordTags[index + 2])
            object.context[8] = nextWord2
            object.context[9] = nextTag2

        return object
