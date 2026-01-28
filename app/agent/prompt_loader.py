from pathlib import Path

SYSTEM_PROMPT_PATH = Path(__file__).parent / "system.txt"

def load_system_prompt() -> str:
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")