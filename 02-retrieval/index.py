import os
import json

from embeddings import get_embedding, cosine_similarity

INDEX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes_sandbox", "notes-index.json")


def _load_index() -> dict:
    if not os.path.exists(INDEX_PATH):
        return {}

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_index(index: dict) -> None:
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f)


def update_note_embedding(filename: str, content: str) -> None:
    index = _load_index()
    index[filename] = get_embedding(content)
    _save_index(index)


def remove_note_embedding(filename: str) -> None:
    index = _load_index()
    index.pop(filename, None)
    _save_index(index)


def search(query: str, top_k: int = 3) -> list:
    index = _load_index()
    if not index:
        return []
    query_vec = get_embedding(query)
    scored = [
        (filename, cosine_similarity(query_vec, vec)) for filename, vec in index.items()
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_k]
