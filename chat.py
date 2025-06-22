#!/usr/bin/env python

import os
from openai import OpenAI


api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not set.")
    exit(1)

client = OpenAI(api_key=api_key)

print("Welcome to terminal GPT chat! Type 'exit' to quit.")

messages = []
summary = None
MAX_MESSAGES = 10


def summarize_history(history):
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


while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        messages.append({"role": "user", "content": user_input})

        # if we have too many messages, summarize oldest ones
        if len(messages) > MAX_MESSAGES:
            # summarize all but last MAX_MESSAGES//2 messages
            to_summarize = messages[:- (MAX_MESSAGES // 2)]
            summary = summarize_history(to_summarize)

            # keep the summary as a system message + recent messages
            messages = [
                {
                    "role": "system",
                    "conent": f"Summary of previous conversation: {summary}"
                }
            ] + messages[-(MAX_MESSAGES // 2):]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content.strip()
        print("GPT:", reply, "\n")

        messages.append({"role": "assistant", "content": reply})

    except KeyboardInterrupt:
        print("\nExiting.")
        break
