from pathlib import Path

CUR_DIR = Path(__file__).parent.absolute()
ROOT_DIR = CUR_DIR.parent.parent.absolute()
DATA_DIR = ROOT_DIR / "data"

OPENING_PUNCTS = [
    "༁",
    "༂",
    "༃",
    "༄",
    "༅",
    "༆",
    "༇",
    "༈",
    "༉",
    "༊",
    "༑",
    "༒",
    "༺",
    "༼",
    "༿",
    "࿐",
    "࿑",
    "࿓",
    "࿔",
    "࿙",
]
CLOSING_PUNCTS = ["།", "༎", "༏", "༐", "༔", "༴", "༻", "༽", "༾", "࿚"]
PUNCTS = OPENING_PUNCTS + CLOSING_PUNCTS
PUNCTS_CHAR_SET = "".join(PUNCTS)


AFFIXES = [
    "འོའང་",
    "འོའམ་",
    "འིའང་",
    "འིའམ་",
    "འིའོ་",
    "འོ་",
    "འང་",
    "འམ་",
    "ས་",
    "ར་",
    "འི་",
    "འོའང",
    "འོའམ",
    "འིའང",
    "འིའམ",
    "འིའོ",
    "འོ",
    "འང",
    "འམ",
    "ས",
    "ར",
    "འི",
]

AFFIXES_WITH_TSEK = [
    "འོའང་",
    "འོའམ་",
    "འིའང་",
    "འིའམ་",
    "འིའོ་",
    "འོ་",
    "འང་",
    "འམ་",
    "ས་",
    "ར་",
    "འི་",
]


AFFIXES_WITHOUT_TSEK = [
    "འོའང",
    "འོའམ",
    "འིའང",
    "འིའམ",
    "འིའོ",
    "འོ",
    "འང",
    "འམ",
    "ས",
    "ར",
    "འི",
]
