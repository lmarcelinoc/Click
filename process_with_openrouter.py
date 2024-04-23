# process_with_openrouter.py

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup OpenAI client with OpenRouter
client = OpenAI(
  base_url=os.getenv("OPENROUTER_ENDPOINT"),
  api_key=os.getenv("OPENROUTER_API_KEY")
)

def get_llm_response(input_text):
    completion = client.chat.completions.create(
      extra_headers={
        "HTTP-Referer": os.getenv("YOUR_SITE_URL"),
        "X-Title": os.getenv("YOUR_APP_NAME"),
      },
      model="openai/gpt-3.5-turbo",
      messages=[{"role": "user", "content": input_text}]
    )
    return completion.choices[0].message.content

def main():
    user_input = "What's the weather like today?"
    response = get_llm_response(user_input)
    print("Response from LLM:", response)

if __name__ == "__main__":
    main()

