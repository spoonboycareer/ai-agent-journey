import os
import math
import requests
from dotenv import load_dotenv

load_dotenv("../.env")

EMBEDDINGS_URL = os.getenv("EMBEDDINGS_URL")
API_KEY = os.getenv("API_KEY")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}


def get_embedding(text: str) -> list:
    payload = {"model": EMBEDDINGS_MODEL, "input": text}
    response = requests.post(EMBEDDINGS_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]


def cosine_similarity(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    if mag_a == 0 or mag_b == 0:
        return 0
    return dot / (mag_a * mag_b)
