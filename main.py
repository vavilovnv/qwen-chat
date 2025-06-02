from openai.types.chat import ChatCompletionMessageParam

from src.open_api import close_client
from src.llm_interaction import ask


def main():
    print("Hello!")
    message_history: list[ChatCompletionMessageParam] = []

    try:
        while True:
            print("Input your question:")
            user_input = input("> ")
            if user_input.lower() in ["exit", "quit", "q"]:
                break

            print("Answer:")
            answer, message_history = ask(
                question=user_input, message_history=message_history
            )
            print(answer)
    except KeyboardInterrupt:
        close_client()
    finally:
        print("Bye!")


if __name__ == "__main__":
    main()
