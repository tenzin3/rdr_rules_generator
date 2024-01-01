from pathlib import Path
from typing import Iterator, Tuple

from rules_generator.RDRPOSTagger.pSCRDRtagger.ExtRDRPOSTagger import train_rdr
from rules_generator.Token import LineTagger
from rules_generator.utility import measure_execution_time


@measure_execution_time(custom_name="RDR Training")
def train_rdr_pipeline(
    tagged_tokens: Iterator[LineTagger],
    rdr_model_file_path: Path,
    threshold: Tuple[int, int] = (20, 20),
):
    train_rdr(tagged_tokens, rdr_model_file_path, threshold)
