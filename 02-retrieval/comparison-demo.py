from embeddings import get_embedding, cosine_similarity

NOTES = {
    "note_a.txt": "Remember to check the oil level and tire pressuer before the road trip.",
    "note_b.txt": "Finished reading a great novel about a lighthouse keeper in Maine.",
}

# QUERY = "What do you need to do for the vehicle maintenance?"
QUERY = "Any note about me completing a story book?"


def keyword_search(query: str, notes: str) -> list:
    query_words = set(query.lower().split())
    matches = []
    for filename, content in notes.items():
        content_words = set(content.lower().split())
        overlap = query_words & content_words
        if overlap:
            matches.append((filename, overlap))
    return matches


def symantic_serach(query: str, notes: str) -> list:
    query_vec = get_embedding(query)
    scores = []
    for filename, content in notes.items():
        note_vec = get_embedding(content)
        score = cosine_similarity(query_vec, note_vec)
        scores.append((filename, score))
    scores.sort(key=lambda pair: pair[1], reverse=True)
    return scores


def main():
    print(f"Query: {QUERY}")
    print("Notes available:")
    for filename, content in NOTES.items():
        print(f"    {filename}: {content}")

    print("\n------ KEYWORD SEARCH ------")
    kw_results = keyword_search(QUERY, NOTES)
    if not kw_results:
        print("No matches. Not one workd in hte query appears in either note.")
    else:
        for filename, overlap in kw_results:
            print(f"{filename} - shared words: {overlap}")

    print("\n------ SEMANTIC SEARCH ------")
    sem_results = symantic_serach(QUERY, NOTES)
    for filename, score in sem_results:
        print(f"{filename} - similarity: {score:.3f}")


if __name__ == "__main__":
    main()
