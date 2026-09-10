from agent import run_agent


def main():
    print("Note Agent - type 'quit' to exit")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"quit", "exit"}:
            break

        if not question:
            continue

        answer = run_agent(question)
        print(f"\nAgent: {answer}")


if __name__ == "__main__":
    main()
