import os
from tools import NOTES_DIR
import index as vector_index


def main():
    if not os.path.exists(NOTES_DIR):
        print("Notes sandbox not found. Nothing to index.")
        return

    filenames = sorted(os.listdir(NOTES_DIR))
    if not filenames:
        print("Notes sandbox is empty, nothing to index.")
        return

    for filename in filenames:
        path = os.path.join(NOTES_DIR, filename)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read

        vector_index.update_note_embedding(filename, content)
        print(f"Indexed: {filename}")

    print(f"\nDone. {len(filename)} note(s) indexed.")


if __name__ == "__main__":
    main()
