import re
from typing import Dict

from rules_generator.RDRPOSTagger.Utility.Utils import getWordTag


def add2WordTagFreqDict(word, tag, inDict):
    if word not in inDict:
        inDict[word] = {}
        inDict[word][tag] = 1
    else:
        if tag not in inDict[word]:
            inDict[word][tag] = 1
        else:
            inDict[word][tag] += 1


def createLexicon(corpusFilePath, fullLexicon):
    if fullLexicon not in ["full", "short"]:
        print("The second parameter gets 'full' or 'short' string-value!")
        print("No lexicon is generated!!!")
        return

    lines = open(corpusFilePath).readlines()
    wordTagCounter: Dict[str, Dict[str, int]] = {}
    for i in range(len(lines)):
        # print i
        pairs = (
            lines[i]
            .strip()
            .replace("“", "''")
            .replace("”", "''")
            .replace('"', "''")
            .split()
        )
        for pair in pairs:
            word, tag = getWordTag(pair)
            if (len(word) >= (len(pair) - 1)) or (len(tag) >= (len(pair) - 1)):
                if fullLexicon == "full":
                    print(
                        "ERROR: The %sth sentence is incorrectly formatted!"
                        % str(i + 1)
                    )
                    # print(pair)
            else:
                add2WordTagFreqDict(word, tag, wordTagCounter)

    from operator import itemgetter

    dictionary = {}

    tagCounter_Alphabet = {}
    tagCounter_CapitalizedWord = {}
    tagCounter_Numeric = {}

    for word in wordTagCounter:
        tagFreq4Word = wordTagCounter[word]
        pairs_list = list(tagFreq4Word.items())
        pairs_list.sort(key=itemgetter(1), reverse=True)
        tag = pairs_list[0][0]

        decodedWord = word
        isCapital = decodedWord[0].isupper()

        if fullLexicon == "full":
            dictionary[word] = tag
        else:  # Get the lexicon without 1-time-occurrence word types
            if (len(pairs_list) == 1 and int(pairs_list[0][1]) > 1) or len(
                pairs_list
            ) > 1:
                dictionary[word] = tag

        if re.search(r"[0-9]+", word) is not None:
            if tag not in tagCounter_Numeric:
                tagCounter_Numeric[tag] = 1
            else:
                tagCounter_Numeric[tag] += 1
        else:
            if isCapital:
                if tag not in tagCounter_CapitalizedWord:
                    tagCounter_CapitalizedWord[tag] = 1
                else:
                    tagCounter_CapitalizedWord[tag] += 1
            else:
                if tag not in tagCounter_Alphabet:
                    tagCounter_Alphabet[tag] = 1
                else:
                    tagCounter_Alphabet[tag] += 1

    from collections import OrderedDict

    dictionary = OrderedDict(sorted(dictionary.items(), key=itemgetter(0)))

    # Get the most frequent tag in the lexicon to label unknown words and numbers
    tagCounter_Alphabet = OrderedDict(
        sorted(tagCounter_Alphabet.items(), key=itemgetter(1), reverse=True)
    )
    tagCounter_CapitalizedWord = OrderedDict(
        sorted(tagCounter_CapitalizedWord.items(), key=itemgetter(1), reverse=True)
    )
    tagCounter_Numeric = OrderedDict(
        sorted(tagCounter_Numeric.items(), key=itemgetter(1), reverse=True)
    )
    tag4UnknWord = list(tagCounter_Alphabet.keys())[0]
    tag4UnknCapitalizedWord = tag4UnknWord
    tag4UnknNum = tag4UnknWord
    if len(tagCounter_CapitalizedWord) > 0:
        tag4UnknCapitalizedWord = list(tagCounter_CapitalizedWord.keys())[0]
    if len(tagCounter_Numeric) > 0:
        tag4UnknNum = list(tagCounter_Numeric.keys())[0]

    # Write to file
    fileSuffix = ".sDict"
    if fullLexicon == "full":
        fileSuffix = ".DICT"
    fileOut = open(corpusFilePath + fileSuffix, "w")

    fileOut.write("TAG4UNKN-WORD " + tag4UnknWord + "\n")
    fileOut.write("TAG4UNKN-CAPITAL " + tag4UnknCapitalizedWord + "\n")
    fileOut.write("TAG4UNKN-NUM " + tag4UnknNum + "\n")
    for key in dictionary:
        fileOut.write(key + " " + dictionary[key] + "\n")

    fileOut.close()
