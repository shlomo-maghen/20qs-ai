from enum import Enum
from pydantic import BaseModel


class Question(BaseModel):
    text: str
    game_id: str
    
class Answer(Enum):
    yes = "yes"
    no = "no"
    unsure = "unsure"

class AnswerOutput(BaseModel):
    answer: Answer
    win: bool
