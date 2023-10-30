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

if __name__ == "__main__":
    print(DATA_DIR)
