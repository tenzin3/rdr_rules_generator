from typing import List

from rules_generator.RDRPOSTagger.SCRDRlearner.SCRDRTreeLearner import SCRDRTreeLearner
from rules_generator.RDRPOSTagger.Utility.Config import THRESHOLD
from rules_generator.Token import LineTagger


def train_rdr(tagged_tokens: List[LineTagger], rdr_model_file_path):
    rdrTree = SCRDRTreeLearner(THRESHOLD[0], THRESHOLD[1])
    rdrTree.learnRDRTree(tagged_tokens)
    rdrTree.writeToFile(str(rdr_model_file_path) + ".RDR")


if __name__ == "__main__":
    pass
