# as this is a small assignment using a common schema file.
# or else i would've created separate files for each schema

from pydantic import BaseModel

# Model to define the output structure
class AnswerResponse(BaseModel):
    question: str
    answer: str