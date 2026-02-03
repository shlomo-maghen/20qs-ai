from enum import Enum
from pydantic import BaseModel
from openai import OpenAI

from models import AnswerOutput

client = OpenAI()

async def ask(text, object) -> AnswerOutput:
    instructions = f"""
    You are answering questions about {object}. 
    You can only answer yes|no|unsure. 
    If the user guesses {object}, that is a win. 
    """.replace("\n", "")
    response = client.responses.parse(
        model="gpt-5-nano",
        reasoning={"effort" : "low"},
        instructions=instructions,
        input=text,
        text_format=AnswerOutput
    )
    return response.output_parsed

