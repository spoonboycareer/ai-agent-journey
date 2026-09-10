import os
from datetime import datetime

import index as vector_index

NOTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes_sandbox", "notes")
os.makedirs(NOTES_DIR, exist_ok=True)


def _safe_path(filename: str) -> str:
    safe_name = os.path.basename(filename)
    path = os.path.join(NOTES_DIR, safe_name)
    if not os.path.abspath(path).startswith(os.path.abspath(NOTES_DIR)):
        raise ValueError("Refused: path escaped the notes sandbox")
    return path


def calculatator(expression: str) -> str:
    allowed = "0123456789+-/*.() "
    if not set(expression) <= allowed:
        return "Error: disallowed character in the expression."

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def get_current_time() -> str:
    return datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")


def list_notes() -> str:
    files = sorted(os.listdir(NOTES_DIR))
    if not files:
        return "No notes yet."
    return "\n".join(files)


def read_note(filename: str) -> str:
    try:
        path = _safe_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    except FileNotFoundError:
        return f"Error: no note called '{filename}'. Use list_notes to see what's available."
    except ValueError as e:
        return f"Error: {e}"


def write_note(filename: str, content: str) -> str:
    try:
        path = _safe_path(filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        vector_index.update_note_embedding(os.path.basename(path), content)
        return f"Saved note '{filename}' ({len(content)} characters) and updated the search index."
    except ValueError as e:
        return f"Error: {e}"


def append_note(filename: str, content: str) -> str:
    try:
        path = _safe_path(filename)
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        with open(path, "r", encoding="utf-8") as f:
            full_content = f.read()

        vector_index.update_note_embedding(os.path.basename(path), full_content)
        return f"Appended to '{filename}' and updated the search index."
    except ValueError as e:
        return "Error: {e}"


def search_note(query: str) -> str:
    result = vector_index.search(query)
    if not result:
        return "No notes are indexed yet. Try list_notes, of add some notes first."
    lines = [f"{filename} (similarity: {score:.2f})" for filename, score in result]
    return "\n".join(lines)


TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "calculatator",
            "description": "Evaluates the basic arithmetic expression e.g. 42 * 3.1415 / 0.707.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
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
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "List the filenames of all saved notes. Use this only when the user wants literal filenames, note when they are asking about note content.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_note",
            "description": "Read the full content of the note by exact filename.",
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
    {
        "type": "function",
        "function": {
            "name": "append_note",
            "description": "Add text to the end of an exising note. Or create new one if the note does not exists yet.",
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
    {
        "type": "function",
        "function": {
            "name": "search_note",
            "description": (
                "Semantically search across all notes for one relevant to "
                "a topic or question. Use this whenever the user asks about "
                "note content rather than giving an exact filename."
            ),
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
]

AVAILABLE_TOOLS = {
    "calculatator": calculatator,
    "get_current_time": get_current_time,
    "list_notes": list_notes,
    "read_note": read_note,
    "write_note": write_note,
    "append_note": append_note,
    "search_note": search_note,
}
