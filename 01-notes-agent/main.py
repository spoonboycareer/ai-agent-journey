from agent import run_agent


def main():
    print("Notes Agent - type 'quit' to exit\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in {"quit", "exit"}:
            break

        if not question:
            continue

        answer = run_agent(question)
        print(f"\nAgent: {answer}\n")


if __name__ == "__main__":
    main()
