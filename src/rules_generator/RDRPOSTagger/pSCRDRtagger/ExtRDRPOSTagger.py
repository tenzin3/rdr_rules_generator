from pathlib import Path
from typing import List, Tuple

from rules_generator.RDRPOSTagger.SCRDRlearner.SCRDRTreeLearner import SCRDRTreeLearner
from rules_generator.Token import LineTagger


def train_rdr(
    tagged_tokens: List[LineTagger],
    rdr_model_file_path: Path,
    threshold: Tuple[int, int],
):
    rdrTree = SCRDRTreeLearner(threshold[0], threshold[1])
    rdrTree.learnRDRTree(tagged_tokens)
    rdrTree.writeToFile(str(rdr_model_file_path) + ".RDR")


if __name__ == "__main__":
    pass
