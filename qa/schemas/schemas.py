# as this is a small assignment using a common schema file.
# or else i would've created separate files for each schema

from typing import List
from pydantic import BaseModel


class AnswerSchema(BaseModel):
    question: str
    answer: str


class AnswerResponse(BaseModel):
    answers: List[AnswerSchema]
