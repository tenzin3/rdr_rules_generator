from typing import Dict, List

from ordered_set import OrderedSet

from rules_generator.RDRPOSTagger.SCRDRlearner.Node import Node
from rules_generator.RDRPOSTagger.SCRDRlearner.Object import getObjectDictionary
from rules_generator.RDRPOSTagger.SCRDRlearner.SCRDRTree import SCRDRTree
from rules_generator.Token import LineTagger


def is_empty_pos(pos: str) -> bool:
    return pos in ["NO_POS", ""]


def get_rule_variations(
    index, start_index, end_index, current_rule, wordrules, posrules, object_pos_list
):
    if start_index == 2 and index == 2 and index == end_index - 1:
        if not is_empty_pos(object_pos_list[index]):
            return [
                current_rule + wordrules[index] + " and " + posrules[index],
            ]
        else:
            return [current_rule + wordrules[index]]
    if index == 2 and index == end_index - 1:
        if not is_empty_pos(object_pos_list[index]):
            return [
                current_rule + wordrules[index],
                current_rule + wordrules[index] + " and " + posrules[index],
            ]
        else:
            return [current_rule + wordrules[index]]
    if index == end_index - 1:
        if not is_empty_pos(object_pos_list[index]):
            return [
                current_rule + posrules[index],
                current_rule + wordrules[index],
                current_rule + wordrules[index] + " and " + posrules[index],
            ]
        else:
            return [current_rule + wordrules[index]]

    pos_rules = []
    if index != 2:
        pos_rules = get_rule_variations(
            index + 1,
            index,
            end_index,
            current_rule + posrules[index] + " and ",
            wordrules,
            posrules,
            object_pos_list,
        )
    word_rules = get_rule_variations(
        index + 1,
        index,
        end_index,
        current_rule + wordrules[index] + " and ",
        wordrules,
        posrules,
        object_pos_list,
    )

    word_and_pos_rules = []
    if not is_empty_pos(object_pos_list[index]):
        word_and_pos_rules = get_rule_variations(
            index + 1,
            index,
            end_index,
            current_rule + wordrules[index] + " and " + posrules[index] + " and ",
            wordrules,
            posrules,
            object_pos_list,
        )
    return pos_rules + word_rules + word_and_pos_rules


# Generate concrete rules based on input object of 5-word window context object
def generateRules(object):

    rule1 = 'object.word == "' + object.word + '"'
    rule2 = 'object.nextWord1 == "' + object.nextWord1 + '"'
    rule3 = 'object.nextWord2 == "' + object.nextWord2 + '"'
    rule4 = 'object.prevWord1 == "' + object.prevWord1 + '"'
    rule5 = 'object.prevWord2 == "' + object.prevWord2 + '"'

    rule6 = 'object.pos == "' + object.pos + '"'
    rule7 = 'object.nextPos1 == "' + object.nextPos1 + '"'
    rule8 = 'object.nextPos2 == "' + object.nextPos2 + '"'
    rule9 = 'object.prevPos1 == "' + object.prevPos1 + '"'
    rule10 = 'object.prevPos2 == "' + object.prevPos2 + '"'

    rules = []
    wordrules = [rule5, rule4, rule1, rule2, rule3]
    posrules = [rule10, rule9, rule6, rule7, rule8]
    object_word_list = [
        object.prevWord2,
        object.prevWord1,
        object.word,
        object.nextWord1,
        object.nextWord2,
    ]

    object_pos_list = [
        object.prevPos2,
        object.prevPos1,
        object.pos,
        object.nextPos1,
        object.nextPos2,
    ]

    for index in range(0, 3):
        if object_word_list[index]:
            if object_word_list[4]:
                rules.extend(
                    get_rule_variations(
                        index, index, 5, "", wordrules, posrules, object_pos_list
                    )
                )
            if object_word_list[3]:
                rules.extend(
                    get_rule_variations(
                        index, index, 4, "", wordrules, posrules, object_pos_list
                    )
                )
            rules.extend(
                get_rule_variations(
                    index, index, 3, "", wordrules, posrules, object_pos_list
                )
            )

    rules_set_dtype = OrderedSet(rules)

    return rules_set_dtype


def countMatching(objects, ruleNotIn):
    counts: Dict[str, int] = {}
    matchedObjects: Dict[str, List] = {}
    for object in objects:
        rules = generateRules(object)
        for rule in rules:
            if rule in ruleNotIn:
                continue
            counts[rule] = counts.setdefault(rule, 0) + 1
            matchedObjects.setdefault(rule, []).append(object)
    return counts, matchedObjects


def satisfy(object, rule):
    return eval(rule)


def fire(rule, cornerstoneCases):
    for object in cornerstoneCases:
        if satisfy(object, rule):
            return True
    return False


def generateRulesFromObjectSet(objects):
    res = []
    for object in objects:
        rules = generateRules(object)
        res += rules
    return res


class SCRDRTreeLearner(SCRDRTree):
    def __init__(self, iThreshold=2, mThreshold=2):
        self.improvedThreshold = iThreshold
        self.matchedThreshold = mThreshold

    # For layer-2 exception structure
    def findMostImprovingRuleForTag(
        self, startTag, correctTag, correctCounts, wrongObjects
    ):
        impCounts, affectedObjects = countMatching(wrongObjects, [])

        maxImp = -1000000
        bestRule = ""
        for rule in impCounts:
            temp = impCounts[rule]
            if rule in correctCounts:
                temp -= correctCounts[rule]

            if temp > maxImp:
                maxImp = temp
                bestRule = rule

        if maxImp == -1000000:
            affectedObjects[bestRule] = []

        return bestRule, maxImp, affectedObjects[bestRule]

    def findMostEfficientRule(self, startTag, objects, correctCounts):
        maxImp = -1000000
        rule = ""
        correctTag = ""
        cornerstoneCases = []

        for tag in objects:
            if tag == startTag:
                continue
            if (
                len(objects[tag]) <= maxImp
                or len(objects[tag]) < self.improvedThreshold
            ):
                continue

            ruleTemp, imp, affectedObjects = self.findMostImprovingRuleForTag(
                startTag, correctTag, correctCounts, objects[tag]
            )
            if imp >= self.improvedThreshold and imp > maxImp:
                maxImp = imp
                rule = ruleTemp
                correctTag = tag
                cornerstoneCases = affectedObjects

        needToCorrectObjects: Dict[str, list] = {}
        errorRaisingObjects = []
        if maxImp > -1000000:
            for tag in objects:
                if tag != correctTag:
                    for object in objects[tag]:
                        if satisfy(object, rule):
                            needToCorrectObjects.setdefault(tag, []).append(object)
                            if tag == startTag:
                                errorRaisingObjects.append(object)

        return (
            rule,
            correctTag,
            maxImp,
            cornerstoneCases,
            needToCorrectObjects,
            errorRaisingObjects,
        )

    def findMostMatchingRule(self, matchingCounts):
        correctTag = ""
        bestRule = ""
        maxCount = -1000000

        for tag in matchingCounts:
            for rule in matchingCounts[tag]:
                if (
                    matchingCounts[tag][rule] >= self.matchedThreshold
                    and matchingCounts[tag][rule] > maxCount
                ):
                    maxCount = matchingCounts[tag][rule]
                    bestRule = rule
                    correctTag = tag

        return bestRule, correctTag

    def buildNodeForObjectSet(self, objects, root):
        cornerstoneCaseRules = generateRulesFromObjectSet(root.cornerstoneCases)

        matchingCounts = {}
        matchingObjects = {}
        for tag in objects:
            matchingCounts[tag], matchingObjects[tag] = countMatching(
                objects[tag], cornerstoneCaseRules
            )

        total = 0
        for tag in objects:
            total += len(objects[tag])

        currentNode = root
        elseChild = False
        while True:
            rule, correctTag = self.findMostMatchingRule(matchingCounts)

            if rule == "":
                break

            cornerstoneCases = matchingObjects[correctTag][rule]

            needToCorrectObjects = {}
            for tag in objects:
                if rule in matchingObjects[tag]:
                    if tag != correctTag:
                        needToCorrectObjects[tag] = matchingObjects[tag][rule]
                    for object in matchingObjects[tag][rule]:
                        rules = generateRules(object)
                        for rule1 in rules:
                            if rule1 not in matchingCounts[tag]:
                                continue
                            matchingCounts[tag][rule1] -= 1

            node = Node(
                rule,
                'object.conclusion = "' + correctTag + '"',
                currentNode,
                None,
                None,
                cornerstoneCases,
            )

            if not elseChild:
                currentNode.exceptChild = node
                elseChild = True
            else:
                currentNode.elseChild = node

            currentNode = node
            self.buildNodeForObjectSet(needToCorrectObjects, currentNode)

    def learnRDRTree(self, tagged_tokens: List[LineTagger]):
        self.root = Node("True", 'object.conclusion = "NN"', None, None, None, [], 0)

        objects = getObjectDictionary(tagged_tokens)

        currentNode = self.root
        for initializedTag in objects:
            # print("===> Building exception rules for tag %s" % initializedTag)
            correctCounts: Dict[str, int] = {}
            for object in objects[initializedTag][initializedTag]:
                rules = generateRules(object)
                for rule in rules:
                    correctCounts[rule] = correctCounts.setdefault(rule, 0) + 1

            node = Node(
                'object.tag == "' + initializedTag + '"',
                'object.conclusion = "' + initializedTag + '"',
                self.root,
                None,
                None,
                [],
                1,
            )

            if self.root.exceptChild is None:
                self.root.exceptChild = node
            else:
                currentNode.elseChild = node

            currentNode = node
            objectSet = objects[initializedTag]

            elseChild = False
            currentNode1 = currentNode
            while True:
                (
                    rule,
                    correctTag,
                    imp,
                    cornerstoneCases,
                    needToCorrectObjects,
                    errorRaisingObjects,
                ) = self.findMostEfficientRule(initializedTag, objectSet, correctCounts)
                if imp < self.improvedThreshold:
                    break

                node = Node(
                    rule,
                    'object.conclusion = "' + correctTag + '"',
                    currentNode,
                    None,
                    None,
                    cornerstoneCases,
                    2,
                )

                if not elseChild:
                    currentNode1.exceptChild = node
                    elseChild = True
                else:
                    currentNode1.elseChild = node

                currentNode1 = node

                for object in cornerstoneCases:
                    objectSet[correctTag].remove(object)

                for tag in needToCorrectObjects:
                    for object in needToCorrectObjects[tag]:
                        objectSet[tag].remove(object)

                for object in errorRaisingObjects:
                    rules = generateRules(object)
                    for rule in rules:
                        correctCounts[rule] -= 1

                self.buildNodeForObjectSet(needToCorrectObjects, currentNode1)
