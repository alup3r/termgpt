#!/usr/bin/env python

import os
from openai import OpenAI


api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not set.")
    exit(1)

client = OpenAI(api_key=api_key)

print("Welcome to terminal GPT chat! Type 'exit' to quit.")


while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )

        print("GPT:", response.choices[0].message.content.strip(), "\n")

    except KeyboardInterrupt:
        print("\nExiting.")
        break
