import re
from typing import List, Union

from pydantic import BaseModel, Field, field_validator


class Token(BaseModel):
    text: str
    pos: Union[str, None] = Field(default=None)
    tag: Union[str, None] = Field(default=None, validate_default=False)

    @field_validator("text")
    @classmethod
    def text_must_be_tibetan(cls, v):
        tibetan_regex = r"^[\u0F00-\u0FFF]+$"
        if not re.match(tibetan_regex, v):
            raise ValueError("Text must contain only Tibetan characters")
        return v

    @field_validator("tag")
    @classmethod
    def tag_must_be_BIUXY(cls, v):
        if not all(char in "BIUXY" for char in v):
            raise ValueError("Tag must contain only BIUXY")
        return v

    def __str__(self):
        return f"Token(text={self.text}, pos={self.pos})"


class LineTagger(BaseModel):
    text: str
    tokens: List[Token] = Field(default=[])
    error: bool = Field(default=False)

    @field_validator("text")
    @classmethod
    def text_must_be_tibetan(cls, v):
        tibetan_regex = r"^[\u0F00-\u0FFF\s\t]+$"
        if not re.match(tibetan_regex, v):
            raise ValueError("Text must contain only Tibetan characters")
        return v
