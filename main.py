from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from enum import Enum
from pathlib import Path
import csv
import random

from models import Question
from openai_service import AnswerOutput, ask

GAME_COUNT = 298
STATIC_PATH = Path(__file__).parent / "static"

app = FastAPI()
templates = Jinja2Templates(directory=str(STATIC_PATH))

def get_thing_from_csv(game_id: int) -> str:
    """Get the thing to guess from things.csv based on game_id (1-indexed)"""
    csv_path = STATIC_PATH / "things.csv"
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader, start=1):
            if idx == game_id:
                return row[0] if row else ""
    return ""


@app.get("/")
async def root():
    game_id = random.randint(1, GAME_COUNT)
    return RedirectResponse(url=f"/game/{game_id}")


@app.get("/game/{game_id}", response_class=HTMLResponse)
async def get_game(game_id: str, request: Request):
    return templates.TemplateResponse("game.html", {"request": request, "game_id": game_id})


@app.get("/game.css")
async def get_css():
    css_path = STATIC_PATH / "style.css"
    return HTMLResponse(content=css_path.read_text(), media_type="text/css")


@app.get("/game.js")
async def get_js():
    js_path = STATIC_PATH / "script.js"
    return HTMLResponse(content=js_path.read_text(), media_type="application/javascript")


@app.post("/ask", response_model=AnswerOutput)
async def ask_question(question: Question):
    thing = get_thing_from_csv(int(question.game_id))
    return await ask(question.text, thing)
