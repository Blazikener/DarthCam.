from gpt4all import GPT4All
from pathlib import Path

# Full path to the model file
model_path = Path(r"C:\Users\abdulahad\Desktop\HackEra\tinyllama-1.1b-chat-v1.0.Q2_K.gguf")

# Check if file exists
if not model_path.exists():
    raise FileNotFoundError(f"Model not found: {model_path}")

# Load the model (convert path to string)
model = GPT4All(model_name=str(model_path), allow_download=False)

# Chat loop
with model.chat_session() as session:
    while True:
        prompt = input("You: ")
        if prompt.lower() in ['exit', 'quit']:
            break
        response = session.generate(prompt)
        print("Bot:", response)
