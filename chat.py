#!/usr/bin/env python

import os

from openai import OpenAI
from termcolor import colored


def summarize_history(history, client):
    """Summarize older messages into one short system message"""
    summary_prompt = (
        "Summarize the following conversation briefly, "
        "so the assistant remembers the key points:\n\n"
    )
    conversation_text = ""
    for msg in history:
        role = msg["role"]
        content = msg["content"]
        conversation_text += f"{role}: {content}\n"
    prompt = summary_prompt + conversation_text

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )
    return response.choices[0].message.content.strip()


def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set.")
        exit(1)

    model_name = "gpt-3.5-turbo"
    client = OpenAI(api_key=api_key)

    print("Welcome to TermGPT!")
    print(f"You are using {colored(model_name, 'green')}")
    print("Type 'exit' to quit.\n")

    messages = []
    summary = None
    MAX_MESSAGES = 10

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in {"exit", "quit"}:
                break

            # reset history
            if user_input.strip() in {"/reset", "/clear"}:
                confirm = input(colored("reset conversation? (y/n): ", 'yellow'))
                if confirm == "y":
                    messages = []
                    summary = None
                    print(colored("history cleared.\n", "green"))
                else:
                    print(colored("reset cancelled.\n", "red"))
                continue
            

            messages.append({"role": "user", "content": user_input})

            # if we have too many messages, summarize oldest ones
            if len(messages) > MAX_MESSAGES:
                # summarize all but last MAX_MESSAGES//2 messages
                to_summarize = messages[:- (MAX_MESSAGES // 2)]
                summary = summarize_history(to_summarize, client)

                # keep the summary as a system message + recent messages
                messages = [
                    {
                        "role": "system",
                        "content": f"Summary of previous conversation: {summary}"
                    }
                ] + messages[-(MAX_MESSAGES // 2):]

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            content = response.choices[0].message.content
            reply = content.strip() if content else ""
            print("GPT:", reply, "\n")

            messages.append({"role": "assistant", "content": reply})

        except KeyboardInterrupt:
            print("\nExiting.")
            break


if __name__ == "__main__":
    main()
