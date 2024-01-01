from pathlib import Path
from typing import Tuple

from rules_generator.config import DATA_DIR
from rules_generator.line_tagging_processor import line_by_line_tagger
from rules_generator.rdr import train_rdr_pipeline
from rules_generator.utility import measure_execution_time


@measure_execution_time(custom_name="Pipeline")
def pipeline(
    training_file_path: Path,
    threshold: Tuple[int, int] = (20, 20),
    split_affixes: bool = True,
):
    gold_corpus = training_file_path.read_text(encoding="utf-8")
    tagged_tokens = line_by_line_tagger(gold_corpus, split_affixes)
    train_rdr_pipeline(tagged_tokens, training_file_path, threshold)


if __name__ == "__main__":
    file_path = DATA_DIR / "txt" / "chojuk.txt"
    pipeline(file_path, (30, 30))
