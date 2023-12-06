from pathlib import Path
from typing import List, Tuple

from rules_generator.config import DATA_DIR
from rules_generator.RDRPOSTagger.pSCRDRtagger.ExtRDRPOSTagger import train_rdr
from rules_generator.Token import LineTagger
from rules_generator.utility import read_tokens_from_json_file


def train_rdr_pipeline(
    tagged_tokens: List[LineTagger],
    rdr_model_file_path: Path,
    threshold: Tuple[int, int] = (20, 20),
):
    print("3.TRAINING RDR STARTED::::>>>>")
    train_rdr(tagged_tokens, rdr_model_file_path, threshold)
    print("3.TRAINING RDR ENDED::::>>>>")


if __name__ == "__main__":
    tokens_tagged_file_path = Path(DATA_DIR) / "tagged_tokens.json"
    tagged_tokens = read_tokens_from_json_file(tokens_tagged_file_path)
    rdr_model_file_path = Path(DATA_DIR) / "rdr_model"
    train_rdr_pipeline(tagged_tokens, rdr_model_file_path, (30, 30))
