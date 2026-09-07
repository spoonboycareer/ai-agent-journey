import os
from datetime import datetime

NOTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes_sandbox")
os.makedirs(NOTES_DIR, exist_ok=True)


def _safe_path(filename: str) -> str:
    safe_name = os.path.basename(filename)
    path = os.path.join(NOTES_DIR, safe_name)

    if not os.path.abspath(path).startswith(os.path.abspath(NOTES_DIR)):
        raise ValueError("Refused: path escapes the notes sanbox.")

    return path


def calculator(expression: str) -> str:
    allowed = set("0123456789+-*/(). ")

    if not set(expression) <= allowed:
        return "Error: disallowed characters in the expression."

    try:
        result = eval(expression, {"__builtin__": {}}, {})
        return str(float(round(result, 2)))
    except Exception as e:
        return f"Error: {e}"


def get_current_time() -> str:
    return datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")


def list_notes() -> str:
    files = sorted(os.listdir(NOTES_DIR))
    if not files:
        return "No notes yet"
    return "\n".join(files)


def read_note(filename: str) -> str:
    try:
        path = _safe_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return (
            f"Error: no note called {filename} exists. "
            "Use list_note to see what's available."
        )
    except ValueError as e:
        return f"Error: {e}"


def write_note(filename: str, content: str) -> str:
    try:
        path = _safe_path(filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Save note '{filename}' ({len(content)} characters)."
    except ValueError as e:
        return f"Error {e}"


TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluates a basic arithmatic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"},
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current local date and time.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "List the filenames of all the saved notes.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_note",
            "description": "Read the full contents of the note by filename",
            "parameters": {
                "type": "object",
                "properties": {"filename": {"type": "string"}},
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_note",
            "description": "Create a new note, or overwrite an existing one, with the given content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["filename", "content"],
            },
        },
    },
]


AVAILABLE_TOOLS = {
    "calculator": calculator,
    "get_current_time": get_current_time,
    "list_notes": list_notes,
    "read_note": read_note,
    "write_note": write_note,
}
