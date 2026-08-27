import ollama

response = ollama.chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "user",
            "content": "Hello! Tell me about AI."
        }
    ]
)

print(response["message"]["content"])