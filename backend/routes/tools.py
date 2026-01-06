from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "tools.json"

@router.get("/")
def get_tools():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        tools = json.load(f)
    return tools
